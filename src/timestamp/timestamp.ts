class Timestamp {
    private seconds: number;
    private nanoseconds: number;
    private isotimestamp: string;

    constructor() {
        this.update();
    }

    private update(): void {
        const now = Date.now();
        this.seconds = Math.floor(now / 1000);
        this.nanoseconds = (now % 1000) * 1000000;
        this.isotimestamp = new Date(this.seconds * 1000).toISOString().slice(0, 19);
    }

    public toUnixMs(): number {
        return this.seconds * 1000 + Math.floor(this.nanoseconds / 1000000);
    }

    public toIso8601(): string {
        return `${this.isotimestamp}.${String(this.nanoseconds).padStart(9, '0')}Z`;
    }

    public toString(): string {
        return this.toIso8601();
    }
}

class EncryptedNode {
    private nodeId: Uint8Array;
    private macAddress: Uint8Array;
    public radius: number;
    public diameter: number;
    public volume: number;
    private timestamp: number;
    public encrypted: boolean;

    constructor(nodeId: string = '', mac: string = '') {
        this.nodeId = this.strToBytes(nodeId, 16);
        this.macAddress = this.parseMac(mac);
        this.timestamp = Math.floor(Date.now() / 1000);
        this.setRadius(1.0);
        this.encrypted = false;
    }

    private strToBytes(str: string, len: number): Uint8Array {
        const bytes = new Uint8Array(len);
        for (let i = 0; i < Math.min(str.length, len); i++) {
            bytes[i] = str.charCodeAt(i);
        }
        return bytes;
    }

    private parseMac(mac: string): Uint8Array {
        const bytes = new Uint8Array(6);
        if (mac) {
            const parts = mac.split(':');
            for (let i = 0; i < Math.min(parts.length, 6); i++) {
                bytes[i] = parseInt(parts[i], 16);
            }
        }
        return bytes;
    }

    public setRadius(r: number): void {
        this.radius = r;
        this.diameter = r * 2.0;
        this.volume = (4.0 / 3.0) * Math.PI * Math.pow(r, 3);
    }

    public encrypt(): void {
        this.nodeId = new Uint8Array(this.nodeId.map(b => b ^ 0xFF));
        this.macAddress = new Uint8Array(this.macAddress.map(b => b ^ 0xFF));
        this.encrypted = true;
    }

    public decrypt(): void {
        this.nodeId = new Uint8Array(this.nodeId.map(b => b ^ 0xFF));
        this.macAddress = new Uint8Array(this.macAddress.map(b => b ^ 0xFF));
        this.encrypted = false;
    }

    public getRadiusBits(): bigint {
        const buffer = new ArrayBuffer(8);
        new DataView(buffer).setFloat64(0, this.radius, false);
        return new DataView(buffer).getBigUint64(0, false);
    }
}

const ts = new Timestamp();
console.log(`Timestamp: ${ts}`);
console.log(`Unix ms: ${ts.toUnixMs()}`);

const node = new EncryptedNode('C2', 'e4:b9:7a:f8:95:1b');
console.log(`\nInitial: radius=${node.radius}, diameter=${node.diameter}, volume=${node.volume}`);

node.setRadius(3.14159);
console.log(`\nWith radius=3.14159:`);
console.log(`Radius: ${node.radius.toPrecision(17)} (64-bit)`);
console.log(`Diameter: ${node.diameter.toPrecision(17)}`);
console.log(`Volume: ${node.volume.toPrecision(17)}`);
console.log(`Radius bits: ${node.getRadiusBits().toString(16).padStart(16, '0')}`);
