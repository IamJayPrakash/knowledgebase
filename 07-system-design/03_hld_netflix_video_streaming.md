# High-Level System Design: Global Video Streaming Architecture (Netflix / YouTube)

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Jab Netflix par koi 4K movie upload hoti hai, toh wo ek single video file nahi rehti.
**Transcoding Pipeline** us movie ko 1000 alag-alag version mein todta hai: 1080p, 720p, 480p, 360p, aur har resolution ko **2-second ke chote chote tukdo (Chunks)** mein kaat deta hai (**HLS / DASH**).
Jab user local metro mein chalta hai aur network kamzor hota hai, video player apne aap 1080p chunk se 480p chunk par switch kar leta hai (**Adaptive Bitrate Streaming**) taaki video buffering na kare! Aur ye chunks user ke sabse paas wale Internet Provider (ISP) ke **Open Connect CDN Cache** se aate hain!

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Scale Requirements**:
   - 250M+ active subscribers globally.
   - Petabytes of video data transmitted every second.
2. **Adaptive Bitrate Streaming (ABR)**:
   - Protocols: HLS (HTTP Live Streaming) and MPEG-DASH.
   - Master manifest file (`playlist.m3u8`) lists bitrates, audio tracks, and subtitles.
   - Player monitors network buffer health and dynamically requests higher/lower bitrate 2-second chunk segments (`.ts` / `.m4s`).
3. **Content Delivery Network (CDN) & Open Connect**:
   - Netflix places physical custom storage appliances (OCAs - Open Connect Appliances) directly inside global Internet Service Provider (ISP) data centers, delivering 95%+ of video traffic locally without traversing internet backbones.
4. **Data Storage Architecture**:
   - Video raw files: Amazon S3 object storage.
   - Metadata & User Viewing History: Cassandra / CockroachDB (distributed wide-column NoSQL).
   - Real-time recommendations: Microservices on AWS, caching via EVCache (distributed memcached).

---

## 📊 3. Visual Architecture Diagram

```
                 GLOBAL VIDEO STREAMING ARCHITECTURE
                 
   [ Creator / Studio ] ──► Raw 4K Master Video ──► AWS S3
                                                        │
                                                        ▼
                                    [ Video Transcoding & Chunking Pipeline ]
                                    (Converts to HLS/DASH 2-second segments)
                                                        │
                                                        ▼
                                    [ Replicate to Edge CDNs / Open Connect ]
                                                        │
                                    ┌───────────────────┴───────────────────┐
                                    ▼                                       ▼
                             [ ISP CDN Node A ]                      [ ISP CDN Node B ]
                                    │                                       │
                                    ▼                                       ▼
                             Client Device                           Client Device
                             (4G Mobile: 720p)                       (Smart TV: 4K HDR)
```
