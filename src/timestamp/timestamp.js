class Timestamp {
    constructor() {
        this.update();
    }

    update() {
        const now = Date.now();
        this.seconds = Math.floor(now / 1000);
        this.nanoseconds = (now % 1000) * 1000000;
        this.isotimestamp = new Date(this.seconds * 1000).toISOString().slice(0, 19);
    }

    toUnixMs() {
        return this.seconds * 1000 + Math.floor(this.nanoseconds / 1000000);
    }

    toIso8601() {
        return `${this.isotimestamp}.${String(this.nanoseconds).padStart(9, '0')}Z`;
    }

    toString() {
        return this.toIso8601();
    }
}

class EncryptedNode {
    constructor(nodeId = '', mac = '') {
        this.nodeId = this.strToBytes(nodeId, 16);
        this.macAddress = this.parseMac(mac);
        this.timestamp = Math.floor(Date.now() / 1000);
        this.setRadius(1.0);
        this.encrypted = false;
    }

    strToBytes(str, len) {
        const bytes = new Uint8Array(len);
        for (let i = 0; i < Math.min(str.length, len); i++) {
            bytes[i] = str.charCodeAt(i);
        }
        return bytes;
    }

    parseMac(mac) {
        const bytes = new Uint8Array(6);
        if (mac) {
            const parts = mac.split(':');
            for (let i = 0; i < Math.min(parts.length, 6); i++) {
                bytes[i] = parseInt(parts[i], 16);
            }
        }
        return bytes;
    }

    setRadius(r) {
        this.radius = r;
        this.diameter = r * 2.0;
        this.volume = (4.0 / 3.0) * Math.PI * Math.pow(r, 3);
    }

    encrypt() {
        this.nodeId = new Uint8Array(this.nodeId.map(b => b ^ 0xFF));
        this.macAddress = new Uint8Array(this.macAddress.map(b => b ^ 0xFF));
        this.encrypted = true;
    }

    decrypt() {
        this.nodeId = new Uint8Array(this.nodeId.map(b => b ^ 0xFF));
        this.macAddress = new Uint8Array(this.macAddress.map(b => b ^ 0xFF));
        this.encrypted = false;
    }

    getRadiusBits() {
        const buffer = new ArrayBuffer(8);
        new DataView(buffer).setFloat64(0, this.radius, false);
        return new DataView(buffer).getBigUint64(0, false);
    }

    toString() {
        return `EncryptedNode(radius=${this.radius.toPrecision(17)}, diameter=${this.diameter.toPrecision(17)}, volume=${this.volume.toPrecision(17)}, encrypted=${this.encrypted})`;
    }
}

const ts = new Timestamp();
console.log(`Timestamp: ${ts}`);
console.log(`Unix ms: ${ts.toUnixMs()}`);

const node = new EncryptedNode('C2', 'e4:b9:7a:f8:95:1b');
console.log(`\nInitial: ${node}`);

node.setRadius(3.14159);
console.log(`\nWith radius=3.14159: ${node}`);
console.log(`Radius bits: ${node.getRadiusBits().toString(16).padStart(16, '0')}`);
