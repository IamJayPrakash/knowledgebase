# Machine Coding: Custom Transform Stream (CSV to JSON Parser)

---

## 🐣 1. Layman's Analogy

Transform stream ek **Pencil Sharpener** ki tarah hai: Ek taraf se aap lakdi ki raw pencil daalte ho (Input CSV chunks), sharpener andar gol ghoomta hai (Transform buffer parsing), aur dusri taraf se sharp sharpened pencil bahar aati hai (Formatted JSON objects stream).

---

## 💻 2. Line-by-Line Commented Code Solution

```javascript
import { Transform } from "node:stream";

/**
 * Custom Transform Stream that converts raw CSV text chunks into JSON lines
 */
export class CsvToJsonStream extends Transform {
  constructor(options = {}) {
    // Line 9: Initialize with objectMode output
    super({ ...options, objectMode: true });
    this.headers = null;
    this.residualBuffer = "";
  }

  // Line 15: _transform is invoked for every incoming buffer chunk
  _transform(chunk, encoding, callback) {
    // Line 17: Combine previous residual text with new chunk text
    const fullText = this.residualBuffer + chunk.toString("utf-8");
    const lines = fullText.split(/
?
/);

    // Line 21: The last element may be an incomplete line; store in residual buffer
    this.residualBuffer = lines.pop() || "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;

      // Line 28: First valid line becomes header keys
      if (!this.headers) {
        this.headers = line.split(",").map((h) => h.trim());
        continue;
      }

      // Line 34: Convert row values to JSON object
      const values = line.split(",").map((v) => v.trim());
      const record = {};
      this.headers.forEach((header, idx) => {
        record[header] = values[idx];
      });

      // Line 41: Push transformed JSON record downstream
      this.push(record);
    }

    // Line 45: Acknowledge chunk processing completion
    callback();
  }

  // Line 49: _flush is called when the readable stream ends
  _flush(callback) {
    // Line 51: Process any lingering line in residualBuffer
    if (this.residualBuffer.trim() && this.headers) {
      const values = this.residualBuffer.split(",").map((v) => v.trim());
      const record = {};
      this.headers.forEach((header, idx) => {
        record[header] = values[idx];
      });
      this.push(record);
    }
    callback();
  }
}
```
