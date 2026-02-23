#ifndef ENCRYPTED_NODE_GEOMETRY_HPP
#define ENCRYPTED_NODE_GEOMETRY_HPP

#include <cstdint>
#include <cstring>
#include <cmath>
#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>
#include <array>

class Timestamp {
public:
    uint64_t seconds;
    uint64_t nanoseconds;
    std::string isotimestamp;

    Timestamp() {
        update();
    }

    void update() {
        struct timespec spec;
        clock_gettime(CLOCK_REALTIME, &spec);
        seconds = static_cast<uint64_t>(spec.tv_sec);
        nanoseconds = static_cast<uint64_t>(spec.tv_nsec);
        
        struct tm tm_info;
        gmtime_r(&spec.tv_sec, &tm_info);
        char buf[64];
        strftime(buf, sizeof(buf), "%Y-%m-%dT%H:%M:%S", &tm_info);
        isotimestamp = buf;
    }

    uint64_t toUnixMs() const {
        return seconds * 1000ULL + nanoseconds / 1000000ULL;
    }

    std::string toIso8601() const {
        std::ostringstream oss;
        oss << isotimestamp << "." << std::setw(9) << std::setfill('0') << nanoseconds << "Z";
        return oss.str();
    }

    std::string toString() const {
        return toIso8601();
    }
};

class EncryptedNode {
public:
    std::array<uint8_t, 16> nodeId;
    std::array<uint8_t, 6> macAddress;
    double radius;
    double diameter;
    double volume;
    uint64_t timestamp;
    bool encrypted;

    EncryptedNode(const std::string& nodeIdStr = "", const std::string& macStr = "") {
        std::memset(nodeId.data(), 0, 16);
        std::memset(macAddress.data(), 0, 6);
        
        for (size_t i = 0; i < std::min(nodeIdStr.size(), size_t(16)); i++) {
            nodeId[i] = static_cast<uint8_t>(nodeIdStr[i]);
        }
        
        if (!macStr.empty()) {
            std::sscanf(macStr.c_str(), "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
                        &macAddress[0], &macAddress[1], &macAddress[2],
                        &macAddress[3], &macAddress[4], &macAddress[5]);
        }
        
        timestamp = static_cast<uint64_t>(std::time(nullptr));
        setRadius(1.0);
        encrypted = false;
    }

    void setRadius(double r) {
        radius = r;
        diameter = r * 2.0;
        volume = (4.0 / 3.0) * M_PI * std::pow(r, 3.0);
    }

    void encrypt() {
        for (auto& b : nodeId) b ^= 0xFF;
        for (auto& b : macAddress) b ^= 0xFF;
        encrypted = true;
    }

    void decrypt() {
        for (auto& b : nodeId) b ^= 0xFF;
        for (auto& b : macAddress) b ^= 0xFF;
        encrypted = false;
    }

    uint64_t getRadiusBits() const {
        uint64_t bits;
        std::memcpy(&bits, &radius, sizeof(bits));
        return bits;
    }

    uint64_t getDiameterBits() const {
        uint64_t bits;
        std::memcpy(&bits, &diameter, sizeof(bits));
        return bits;
    }

    uint64_t getVolumeBits() const {
        uint64_t bits;
        std::memcpy(&bits, &volume, sizeof(bits));
        return bits;
    }

    std::string toString() const {
        std::ostringstream oss;
        oss << "EncryptedNode(radius=" << std::setprecision(17) << radius 
            << ", diameter=" << diameter << ", volume=" << volume 
            << ", encrypted=" << std::boolalpha << encrypted << ")";
        return oss.str();
    }
};

#endif
