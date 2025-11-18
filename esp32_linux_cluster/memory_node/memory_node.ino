/*
 * ESP32 Linux Cluster - Memory Node
 *
 * This node acts as distributed RAM for the master node.
 * It receives memory read/write commands via I2C and stores data in flash/SRAM.
 *
 * Hardware: ESP32 Dev1 (WROOM)
 * Role: Distributed memory slave
 */

#include <Wire.h>
#include <SPIFFS.h>

// ===== CONFIGURATION =====
// Set this address for each memory node (0x10, 0x11, 0x12)
#define NODE_ADDRESS 0x10  // CHANGE THIS FOR EACH NODE!

#define I2C_SDA 21
#define I2C_SCL 22

// Memory configuration
#define MEMORY_SIZE (4 * 1024 * 1024)  // 4MB virtual memory
#define SRAM_CACHE_SIZE (128 * 1024)    // 128KB fast cache in SRAM
#define FLASH_STORAGE_SIZE (3 * 1024 * 1024)  // 3MB in SPIFFS

// ===== MEMORY COMMANDS =====
enum MemCommand {
  CMD_WRITE = 0x01,
  CMD_READ = 0x02,
  CMD_STATUS = 0x03,
  CMD_INIT = 0x04,
  CMD_PING = 0x05
};

// ===== MEMORY STORAGE =====
uint8_t sramCache[SRAM_CACHE_SIZE];  // Fast SRAM cache
uint32_t cacheStartAddr = 0;
bool cacheValid = false;

// I2C communication buffers
uint8_t i2cCommand = 0;
uint32_t pendingAddress = 0;
uint16_t pendingLength = 0;
uint8_t i2cBuffer[256];
volatile bool commandReady = false;

// Statistics
struct Stats {
  uint32_t totalReads;
  uint32_t totalWrites;
  uint32_t cacheHits;
  uint32_t cacheMisses;
  uint32_t i2cErrors;
} stats = {0};

// ===== I2C HANDLERS =====

void onI2CReceive(int numBytes) {
  if (numBytes < 1) return;

  i2cCommand = Wire.read();

  switch (i2cCommand) {
    case CMD_PING:
      // Just acknowledge
      break;

    case CMD_WRITE:
      if (numBytes >= 7) {  // cmd + 4 bytes addr + 2 bytes length
        pendingAddress = ((uint32_t)Wire.read() << 24) |
                        ((uint32_t)Wire.read() << 16) |
                        ((uint32_t)Wire.read() << 8) |
                        Wire.read();
        pendingLength = ((uint16_t)Wire.read() << 8) | Wire.read();

        // Read data into buffer
        int idx = 0;
        while (Wire.available() && idx < sizeof(i2cBuffer)) {
          i2cBuffer[idx++] = Wire.read();
        }

        commandReady = true;
      }
      break;

    case CMD_READ:
      if (numBytes >= 7) {
        pendingAddress = ((uint32_t)Wire.read() << 24) |
                        ((uint32_t)Wire.read() << 16) |
                        ((uint32_t)Wire.read() << 8) |
                        Wire.read();
        pendingLength = ((uint16_t)Wire.read() << 8) | Wire.read();

        commandReady = true;
      }
      break;

    case CMD_STATUS:
      commandReady = true;
      break;

    default:
      stats.i2cErrors++;
      break;
  }
}

void onI2CRequest() {
  switch (i2cCommand) {
    case CMD_READ:
      // Send requested data
      if (pendingLength > 0) {
        uint8_t buffer[32];
        size_t toSend = min((size_t)32, (size_t)pendingLength);

        if (readMemory(pendingAddress, buffer, toSend)) {
          Wire.write(buffer, toSend);
        } else {
          // Send zeros on error
          memset(buffer, 0, toSend);
          Wire.write(buffer, toSend);
        }
      }
      break;

    case CMD_STATUS:
      // Send status bytes
      Wire.write(0x01);  // Status: OK
      Wire.write((stats.totalReads >> 8) & 0xFF);
      Wire.write(stats.totalReads & 0xFF);
      Wire.write((stats.totalWrites >> 8) & 0xFF);
      Wire.write(stats.totalWrites & 0xFF);
      break;

    case CMD_PING:
      Wire.write(0xAA);  // Acknowledge
      break;
  }
}

// ===== MEMORY OPERATIONS =====

bool writeMemory(uint32_t address, uint8_t* data, size_t length) {
  if (address + length > MEMORY_SIZE) {
    return false;
  }

  stats.totalWrites++;

  // Write to SRAM cache if in range
  if (address >= cacheStartAddr && address + length <= cacheStartAddr + SRAM_CACHE_SIZE) {
    memcpy(&sramCache[address - cacheStartAddr], data, length);
    cacheValid = true;
    stats.cacheHits++;
    return true;
  }

  // Write to SPIFFS (slower)
  stats.cacheMisses++;
  char filename[32];
  sprintf(filename, "/mem_%08X.bin", address / 4096);  // 4KB blocks

  File file = SPIFFS.open(filename, "w");
  if (!file) {
    return false;
  }

  file.write(data, length);
  file.close();
  return true;
}

bool readMemory(uint32_t address, uint8_t* buffer, size_t length) {
  if (address + length > MEMORY_SIZE) {
    return false;
  }

  stats.totalReads++;

  // Read from SRAM cache if in range
  if (cacheValid && address >= cacheStartAddr &&
      address + length <= cacheStartAddr + SRAM_CACHE_SIZE) {
    memcpy(buffer, &sramCache[address - cacheStartAddr], length);
    stats.cacheHits++;
    return true;
  }

  // Read from SPIFFS
  stats.cacheMisses++;
  char filename[32];
  sprintf(filename, "/mem_%08X.bin", address / 4096);

  if (!SPIFFS.exists(filename)) {
    // Return zeros for uninitialized memory
    memset(buffer, 0, length);
    return true;
  }

  File file = SPIFFS.open(filename, "r");
  if (!file) {
    return false;
  }

  file.read(buffer, length);
  file.close();
  return true;
}

// ===== SETUP & LOOP =====

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n\n");
  Serial.println("╔════════════════════════════════════╗");
  Serial.println("║ ESP32 LINUX CLUSTER - MEMORY NODE  ║");
  Serial.println("╚════════════════════════════════════╝");
  Serial.printf("Node Address: 0x%02X\n", NODE_ADDRESS);

  // Initialize SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("✗ SPIFFS initialization failed!");
  } else {
    Serial.println("✓ SPIFFS initialized");
    Serial.printf("  Total: %d bytes\n", SPIFFS.totalBytes());
    Serial.printf("  Used: %d bytes\n", SPIFFS.usedBytes());
  }

  // Initialize I2C as slave
  Wire.begin(NODE_ADDRESS, I2C_SDA, I2C_SCL, 0);
  Wire.onReceive(onI2CReceive);
  Wire.onRequest(onI2CRequest);

  Serial.println("✓ I2C slave initialized");
  Serial.println("\n=== Memory Node Ready ===");
  Serial.println("Waiting for commands from master...\n");
}

void loop() {
  // Process pending commands
  if (commandReady) {
    commandReady = false;

    switch (i2cCommand) {
      case CMD_WRITE:
        writeMemory(pendingAddress, i2cBuffer, pendingLength);
        Serial.printf("WRITE: addr=0x%08X len=%d\n", pendingAddress, pendingLength);
        break;

      case CMD_READ:
        Serial.printf("READ:  addr=0x%08X len=%d\n", pendingAddress, pendingLength);
        break;

      case CMD_STATUS:
        Serial.println("STATUS request");
        break;
    }
  }

  // Periodic status
  static unsigned long lastStatus = 0;
  if (millis() - lastStatus > 10000) {
    Serial.println("\n--- Memory Node Status ---");
    Serial.printf("Reads: %u | Writes: %u\n", stats.totalReads, stats.totalWrites);
    Serial.printf("Cache hits: %u | misses: %u\n", stats.cacheHits, stats.cacheMisses);
    Serial.printf("I2C errors: %u\n", stats.i2cErrors);

    if (stats.totalReads + stats.totalWrites > 0) {
      float hitRate = (float)stats.cacheHits / (stats.cacheHits + stats.cacheMisses) * 100;
      Serial.printf("Cache hit rate: %.1f%%\n", hitRate);
    }

    lastStatus = millis();
  }

  delay(10);
}
