use std::time::{SystemTime, UNIX_EPOCH};
use std::mem::transmute;

pub struct Timestamp {
    pub seconds: u64,
    pub nanoseconds: u64,
    pub isotimestamp: String,
}

impl Timestamp {
    pub fn now() -> Timestamp {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap();
        
        let secs = now.as_secs();
        let nanos = now.subsec_nanos();
        
        let dt = chrono::Utc::now();
        let isotimestamp = dt.format("%Y-%m-%dT%H:%M:%S").to_string();
        
        Timestamp {
            seconds: secs,
            nanoseconds: nanos as u64,
            isotimestamp,
        }
    }
    
    pub fn to_unix_ms(&self) -> u64 {
        self.seconds * 1000 + (self.nanoseconds / 1_000_000) as u64
    }
    
    pub fn to_iso8601(&self) -> String {
        format!("{}.{:09}Z", self.isotimestamp, self.nanoseconds)
    }
}

#[derive(Clone)]
pub struct EncryptedNode {
    pub node_id: [u8; 16],
    pub mac_address: [u8; 6],
    pub radius: f64,
    pub diameter: f64,
    pub volume: f64,
    pub timestamp: u64,
    pub}

impl EncryptedNode {
    pub encrypted: bool,
 fn new(node_id: &str, mac: &str) -> EncryptedNode {
        let mut nid = [0u8; 16];
        let bytes = node_id.as_bytes();
        for (i, &b) in bytes.iter().take(16).enumerate() {
            nid[i] = b;
        }
        
        let mut mac_addr = [0u8; 6];
        if !mac.is_empty() {
            let parts: Vec<&str> = mac.split(':').collect();
            for (i, part) in parts.iter().take(6).enumerate() {
                mac_addr[i] = u8::from_str_radix(part, 16).unwrap_or(0);
            }
        }
        
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let mut node = EncryptedNode {
            node_id: nid,
            mac_address: mac_addr,
            radius: 1.0,
            diameter: 2.0,
            volume: (4.0 / 3.0) * std::f64::consts::PI * 1.0_f64.powi(3),
            timestamp,
            encrypted: false,
        };
        
        node
    }
    
    pub fn set_radius(&mut self, r: f64) {
        self.radius = r;
        self.diameter = r * 2.0;
        self.volume = (4.0 / 3.0) * std::f64::consts::PI * r.powi(3);
    }
    
    pub fn encrypt(&mut self) {
        for b in &mut self.node_id {
            *b ^= 0xFF;
        }
        for b in &mut self.mac_address {
            *b ^= 0xFF;
        }
        self.encrypted = true;
    }
    
    pub fn decrypt(&mut self) {
        for b in &mut self.node_id {
            *b ^= 0xFF;
        }
        for b in &mut self.mac_address {
            *b ^= 0xFF;
        }
        self.encrypted = false;
    }
    
    pub fn get_radius_bits(&self) -> u64 {
        unsafe { transmute::<f64, u64>(self.radius) }
    }
    
    pub fn get_diameter_bits(&self) -> u64 {
        unsafe { transmute::<f64, u64>(self.diameter) }
    }
    
    pub fn get_volume_bits(&self) -> u64 {
        unsafe { transmute::<f64, u64>(self.volume) }
    }
}

fn main() {
    let ts = Timestamp::now();
    println!("Timestamp: {}", ts.to_iso8601());
    println!("Unix ms: {}", ts.to_unix_ms());
    
    let mut node = EncryptedNode::new("C2E4B97AF8951B", "e4:b9:7a:f8:95:1b");
    println!("\nNode: Radius={:.17}, Diameter={:.17}, Volume={:.17}", 
             node.radius, node.diameter, node.volume);
    println!("Radius bits: {:016x}", node.get_radius_bits());
    
    node.set_radius(42.0);
    println!("\nAfter set_radius(42.0):");
    println!("Radius: {:.17} (64-bit)", node.radius);
    println!("Diameter: {:.17}", node.diameter);
    println!("Volume: {:.17}", node.volume);
    
    node.encrypt();
    println!("\nEncrypted: {}", node.encrypted);
    node.decrypt();
    println!("Decrypted: {}", node.encrypted);
}
