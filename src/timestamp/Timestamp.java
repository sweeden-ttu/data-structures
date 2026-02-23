package com.datastructures;

import java.time.Instant;
import java.nio.ByteBuffer;
import java.util.Arrays;

public class Timestamp {
    private long seconds;
    private long nanoseconds;
    private String isoTimestamp;

    public Timestamp() {
        update();
    }

    private void update() {
        Instant now = Instant.now();
        this.seconds = now.getEpochSecond();
        this.nanoseconds = now.getNano();
        this.isoTimestamp = now.toString().substring(0, 19);
    }

    public long toUnixMs() {
        return seconds * 1000 + nanoseconds / 1_000_000;
    }

    public String toIso8601() {
        return String.format("%s.%09dZ", isoTimestamp, nanoseconds);
    }

    public String toString() {
        return toIso8601();
    }
}

public class EncryptedNode {
    private byte[] nodeId;
    private byte[] macAddress;
    private double radius;
    private double diameter;
    private double volume;
    private long timestamp;
    private boolean encrypted;

    public EncryptedNode(String nodeId, String mac) {
        this.nodeId = nodeId.getBytes(java.nio.charset.StandardCharsets.UTF_8);
        if (this.nodeId.length < 16) {
            this.nodeId = Arrays.copyOf(this.nodeId, 16);
        }
        
        this.macAddress = parseMac(mac);
        this.timestamp = Instant.now().getEpochSecond();
        setRadius(1.0);
        this.encrypted = false;
    }

    private byte[] parseMac(String mac) {
        byte[] result = new byte[6];
        if (mac != null && !mac.isEmpty()) {
            String[] parts = mac.split(":");
            for (int i = 0; i < Math.min(parts.length, 6); i++) {
                result[i] = (byte) Integer.parseInt(parts[i], 16);
            }
        }
        return result;
    }

    public void setRadius(double r) {
        this.radius = r;
        this.diameter = r * 2.0;
        this.volume = (4.0 / 3.0) * Math.PI * Math.pow(r, 3);
    }

    public void encrypt() {
        for (int i = 0; i < nodeId.length; i++) {
            nodeId[i] ^= 0xFF;
        }
        for (int i = 0; i < macAddress.length; i++) {
            macAddress[i] ^= 0xFF;
        }
        this.encrypted = true;
    }

    public void decrypt() {
        for (int i = 0; i < nodeId.length; i++) {
            nodeId[i] ^= 0xFF;
        }
        for (int i = 0; i < macAddress.length; i++) {
            macAddress[i] ^= 0xFF;
        }
        this.encrypted = false;
    }

    public long getRadiusBits() {
        return Double.doubleToLongBits(radius);
    }

    public long getDiameterBits() {
        return Double.doubleToLongBits(diameter);
    }

    public long getVolumeBits() {
        return Double.doubleToLongBits(volume);
    }

    public String toString() {
        return String.format(
            "EncryptedNode(radius=%.17g, diameter=%.17g, volume=%.17g, encrypted=%b)",
            radius, diameter, volume, encrypted
        );
    }

    public static void main(String[] args) {
        Timestamp ts = new Timestamp();
        System.out.println("Timestamp: " + ts);
        System.out.println("Unix ms: " + ts.toUnixMs());

        EncryptedNode node = new EncryptedNode("C2", "e4:b9:7a:f8:95:1b");
        System.out.println("\nInitial: " + node);
        
        node.setRadius(3.14159);
        System.out.println("\nWith radius=3.14159: " + node);
        System.out.println("Radius bits: " + String.format("%016x", node.getRadiusBits()));
    }
}
