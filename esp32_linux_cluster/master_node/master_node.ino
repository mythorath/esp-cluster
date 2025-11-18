/*
 * ESP32 Linux Cluster - Master Node
 *
 * This node runs the RISC-V emulator and coordinates the cluster.
 * It uses I2C to communicate with memory nodes for distributed RAM.
 *
 * Hardware: ESP32 Dev1 (WROOM)
 * Role: CPU emulation, cluster coordination
 */

#include <Wire.h>
#include <WiFi.h>
#include <PubSubClient.h>

// ===== CONFIGURATION =====
#define I2C_SDA 21
#define I2C_SCL 22
#define I2C_FREQ 400000  // 400kHz Fast Mode

// Memory node I2C addresses
#define MEM_NODE_1_ADDR 0x10
#define MEM_NODE_2_ADDR 0x11
#define MEM_NODE_3_ADDR 0x12
#define NUM_MEM_NODES 3

// WiFi Configuration (for MQTT/Broccoli)
const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASSWORD";
const char* MQTT_BROKER = "192.168.1.100";
const int MQTT_PORT = 1883;

// ===== MEMORY MANAGEMENT =====
struct MemoryNode {
  uint8_t address;
  bool available;
  uint32_t capacity;  // 4MB per node
  uint32_t used;
};

MemoryNode memoryNodes[NUM_MEM_NODES] = {
  {MEM_NODE_1_ADDR, false, 4 * 1024 * 1024, 0},
  {MEM_NODE_2_ADDR, false, 4 * 1024 * 1024, 0},
  {MEM_NODE_3_ADDR, false, 4 * 1024 * 1024, 0}
};

// ===== I2C MEMORY OPERATIONS =====

// Commands for memory nodes
enum MemCommand {
  CMD_WRITE = 0x01,
  CMD_READ = 0x02,
  CMD_STATUS = 0x03,
  CMD_INIT = 0x04,
  CMD_PING = 0x05
};

// Write data to distributed memory
bool writeDistributedMemory(uint32_t address, uint8_t* data, size_t length) {
  // Determine which memory node to use based on address
  int nodeIndex = (address / (4 * 1024 * 1024)) % NUM_MEM_NODES;
  uint32_t localAddress = address % (4 * 1024 * 1024);

  if (!memoryNodes[nodeIndex].available) {
    Serial.printf("Memory node %d not available!\n", nodeIndex);
    return false;
  }

  // Send write command over I2C
  Wire.beginTransmission(memoryNodes[nodeIndex].address);
  Wire.write(CMD_WRITE);
  Wire.write((localAddress >> 24) & 0xFF);
  Wire.write((localAddress >> 16) & 0xFF);
  Wire.write((localAddress >> 8) & 0xFF);
  Wire.write(localAddress & 0xFF);
  Wire.write((length >> 8) & 0xFF);
  Wire.write(length & 0xFF);

  // Write data in chunks (I2C buffer limit)
  size_t written = 0;
  while (written < length) {
    size_t chunk = min((size_t)32, length - written);
    Wire.write(data + written, chunk);
    written += chunk;
  }

  uint8_t error = Wire.endTransmission();
  return (error == 0);
}

// Read data from distributed memory
bool readDistributedMemory(uint32_t address, uint8_t* buffer, size_t length) {
  int nodeIndex = (address / (4 * 1024 * 1024)) % NUM_MEM_NODES;
  uint32_t localAddress = address % (4 * 1024 * 1024);

  if (!memoryNodes[nodeIndex].available) {
    return false;
  }

  // Send read command
  Wire.beginTransmission(memoryNodes[nodeIndex].address);
  Wire.write(CMD_READ);
  Wire.write((localAddress >> 24) & 0xFF);
  Wire.write((localAddress >> 16) & 0xFF);
  Wire.write((localAddress >> 8) & 0xFF);
  Wire.write(localAddress & 0xFF);
  Wire.write((length >> 8) & 0xFF);
  Wire.write(length & 0xFF);
  Wire.endTransmission();

  // Request data
  size_t read = 0;
  while (read < length) {
    size_t chunk = min((size_t)32, length - read);
    Wire.requestFrom(memoryNodes[nodeIndex].address, chunk);

    while (Wire.available() && read < length) {
      buffer[read++] = Wire.read();
    }
  }

  return (read == length);
}

// Ping all memory nodes
void discoverMemoryNodes() {
  Serial.println("\n=== Discovering Memory Nodes ===");

  for (int i = 0; i < NUM_MEM_NODES; i++) {
    Wire.beginTransmission(memoryNodes[i].address);
    Wire.write(CMD_PING);
    uint8_t error = Wire.endTransmission();

    if (error == 0) {
      memoryNodes[i].available = true;
      Serial.printf("✓ Memory Node %d (0x%02X) - ONLINE\n", i, memoryNodes[i].address);
    } else {
      memoryNodes[i].available = false;
      Serial.printf("✗ Memory Node %d (0x%02X) - OFFLINE\n", i, memoryNodes[i].address);
    }
  }
}

// ===== WIFI & MQTT =====
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed!");
  }
}

void setupMQTT() {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  // Add callback for Broccoli integration
}

// ===== MAIN SETUP & LOOP =====

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n\n");
  Serial.println("╔════════════════════════════════════╗");
  Serial.println("║  ESP32 LINUX CLUSTER - MASTER NODE ║");
  Serial.println("╚════════════════════════════════════╝");

  // Initialize I2C as master
  Wire.begin(I2C_SDA, I2C_SCL, I2C_FREQ);
  Serial.printf("I2C initialized (SDA:%d, SCL:%d, %dkHz)\n", I2C_SDA, I2C_SCL, I2C_FREQ/1000);

  // Discover memory nodes
  delay(500);
  discoverMemoryNodes();

  // Initialize WiFi and MQTT
  setupWiFi();
  if (WiFi.status() == WL_CONNECTED) {
    setupMQTT();
  }

  // Test distributed memory
  testDistributedMemory();

  Serial.println("\n=== Master Node Ready ===");
}

void testDistributedMemory() {
  Serial.println("\n=== Testing Distributed Memory ===");

  // Test data
  uint8_t testData[] = "Hello from ESP32 Linux Cluster!";
  uint8_t readBuffer[64] = {0};

  // Write to memory node 0
  Serial.print("Writing test data... ");
  if (writeDistributedMemory(0x1000, testData, sizeof(testData))) {
    Serial.println("OK");
  } else {
    Serial.println("FAILED");
    return;
  }

  delay(100);

  // Read back
  Serial.print("Reading test data... ");
  if (readDistributedMemory(0x1000, readBuffer, sizeof(testData))) {
    Serial.println("OK");
    Serial.printf("Data: %s\n", readBuffer);

    if (memcmp(testData, readBuffer, sizeof(testData)) == 0) {
      Serial.println("✓ Memory test PASSED!");
    } else {
      Serial.println("✗ Memory test FAILED - data mismatch!");
    }
  } else {
    Serial.println("FAILED");
  }
}

void loop() {
  // Main loop - will contain RISC-V emulator execution

  // For now, just heartbeat
  static unsigned long lastHeartbeat = 0;
  if (millis() - lastHeartbeat > 5000) {
    Serial.println("💓 Master node heartbeat");

    // Print memory node status
    int available = 0;
    for (int i = 0; i < NUM_MEM_NODES; i++) {
      if (memoryNodes[i].available) available++;
    }
    Serial.printf("Memory nodes: %d/%d online\n", available, NUM_MEM_NODES);

    lastHeartbeat = millis();
  }

  // Handle MQTT if connected
  if (mqttClient.connected()) {
    mqttClient.loop();
  }

  delay(100);
}
