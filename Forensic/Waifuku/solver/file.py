import frida
import sys

frida_script = """
Interceptor.attach(Module.getExportByName("kernel32.dll", "CreateFileW"), {
    onEnter: function (args) {
        this.fileName = args[0].readUtf16String();
        this.access = args[1].toInt32();
        this.mode = args[2].toInt32();
    },
    onLeave: function (retval) {
        if (retval.toInt32() !== -1) {
            console.log("[+] CreateFileW called:");
            console.log("    File name: " + this.fileName);
            console.log("    Access: " + this.access);
        }
    }
});

var WriteFile = Module.getExportByName('kernel32.dll', 'WriteFile');
Interceptor.attach(WriteFile, {
    onEnter: function (args) {
        this.handle = args[0];
        this.buffer = args[1];
        this.bytesToWrite = args[2].toInt32();
        this.bytesWritten = args[3];
        
        if (this.bytesToWrite > 0) {
            var buf = Memory.readByteArray(this.buffer, this.bytesToWrite);
            
            console.log('\\n[+] WriteFile called:');
            console.log('    Handle: ' + this.handle);
            console.log('    Bytes to write: ' + this.bytesToWrite);
            
            console.log('    Buffer content (hex):');
            console.log(hexdump(buf, { offset: 0, length: Math.min(this.bytesToWrite, 256), header: true, ansi: false }));
            
            try {
                var str = Memory.readUtf8String(this.buffer, this.bytesToWrite);
                if (str && str.length > 0) {
                    console.log('    Buffer as string: ' + str);
                }
            } catch (e) {
            }
        }
    }
});
"""


def on_message(message, data):
    if message["type"] == "send":
        print(message["payload"])
    else:
        print(message)


if __name__ == "__main__":
    pid = frida.spawn("main.exe")
    session = frida.attach(pid)
    script = session.create_script(frida_script)
    script.on("message", on_message)
    script.load()
    frida.resume(pid)
    print("[*] Press Ctrl+C to stop")
    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        print("\n[*] Exiting...")
