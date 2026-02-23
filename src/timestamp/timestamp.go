package timestamp

import (
	"encoding/binary"
	"fmt"
	"math"
	"time"
)

type Timestamp struct {
	Seconds      uint64
	Nanoseconds  uint64
	IsoTimestamp string
}

func Now() *Timestamp {
	now := time.Now()
	ts := &Timestamp{
		Seconds:      uint64(now.Unix()),
		Nanoseconds:  uint64(now.Nanosecond()),
		IsoTimestamp: now.UTC().Format("2006-01-02T15:04:05"),
	}
	return ts
}

func (t *Timestamp) ToUnixMs() uint64 {
	return t.Seconds*1000 + uint64(t.Nanoseconds)/1_000_000
}

func (t *Timestamp) ToISO8601() string {
	return fmt.Sprintf("%s.%09dZ", t.IsoTimestamp, t.Nanoseconds)
}

type EncryptedNode struct {
	NodeID     [16]byte
	MacAddress [6]byte
	Radius     float64
	Diameter   float64
	Volume     float64
	Timestamp  uint64
	Encrypted  bool
}

func NewEncryptedNode(nodeID string, mac string) *EncryptedNode {
	var nid [16]byte
	copy(nid[:], []byte(nodeID))
	
	var macAddr [6]byte
	if mac != "" {
		fmt.Sscanf(mac, "%x:%x:%x:%x:%x:%x", 
			&macAddr[0], &macAddr[1], &macAddr[2], 
			&macAddr[3], &macAddr[4], &macAddr[5])
	}
	
	node := &EncryptedNode{
		NodeID:     nid,
		MacAddress: macAddr,
		Timestamp:  uint64(time.Now().Unix()),
	}
	node.SetRadius(1.0)
	return node
}

func (n *EncryptedNode) SetRadius(r float64) {
	n.Radius = r
	n.Diameter = r * 2.0
	n.Volume = (4.0 / 3.0) * math.Pi * math.Pow(r, 3)
}

func (n *EncryptedNode) Encrypt() {
	for i := range n.NodeID {
		n.NodeID[i] ^= 0xFF
	}
	for i := range n.MacAddress {
		n.MacAddress[i] ^= 0xFF
	}
	n.Encrypted = true
}

func (n *EncryptedNode) Decrypt() {
	for i := range n.NodeID {
		n.NodeID[i] ^= 0xFF
	}
	for i := range n.MacAddress {
		n.MacAddress[i] ^= 0xFF
	}
	n.Encrypted = false
}

func (n *EncryptedNode) GetRadiusBits() uint64 {
	bits := math.Float64bits(n.Radius)
	return bits
}

func (n *EncryptedNode) GetDiameterBits() uint64 {
	return math.Float64bits(n.Diameter)
}

func (n *EncryptedNode) GetVolumeBits() uint64 {
	return math.Float64bits(n.Volume)
}

func main() {
	ts := Now()
	fmt.Printf("Timestamp: %s\n", ts.ToISO8601())
	fmt.Printf("Unix ms: %d\n", ts.ToUnixMs())
	
	node := NewEncryptedNode("C2E4B97AF8951B", "e4:b9:7a:f8:95:1b")
	fmt.Printf("\nNode: Radius=%.17g, Diameter=%.17g, Volume=%.17g\n", 
		node.Radius, node.Diameter, node.Volume)
	fmt.Printf("Radius bits: %016x\n", node.GetRadiusBits())
	
	node.SetRadius(42.0)
	fmt.Printf("\nAfter SetRadius(42.0):\n")
	fmt.Printf("Radius: %.17g (64-bit)\n", node.Radius)
	fmt.Printf("Diameter: %.17g\n", node.Diameter)
	fmt.Printf("Volume: %.17g\n", node.Volume)
	
	node.Encrypt()
	fmt.Printf("\nEncrypted: %v\n", node.Encrypted)
	node.Decrypt()
	fmt.Printf("Decrypted: %v\n", node.Encrypted)
}
