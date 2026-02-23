#include <iostream>
#include "timestamp/encrypted_node.hpp"

int main() {
    Timestamp ts;
    std::cout << "Timestamp: " << ts.toString() << std::endl;
    std::cout << "Unix ms: " << ts.toUnixMs() << std::endl;

    EncryptedNode node("C2", "e4:b9:7a:f8:95:1b");
    std::cout << "\nInitial: " << node.toString() << std::endl;
    std::cout << "Radius bits: " << std::hex << std::setfill('0') << std::setw(16) << node.getRadiusBits() << std::dec << std::endl;

    node.setRadius(3.14159);
    std::cout << "\nWith radius=3.14159: " << node.toString() << std::endl;
    std::cout << "Radius bits: " << std::hex << std::setfill('0') << std::setw(16) << node.getRadiusBits() << std::dec << std::endl;

    return 0;
}
