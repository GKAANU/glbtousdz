# GLB to USDZ – Apify Actor

GLB 3D AR modellerini Apple USDZ formatına çeviren Apify actor’ü. [Google’ın usd_from_gltf](https://github.com/google/usd_from_gltf) aracını kullanır; çıktı iOS AR Quick Look ile uyumludur.

## Girdi (Input)

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `glbUrl` | string | *biri zorunlu* | Dönüştürülecek GLB dosyasının public URL’i |
| `glbBase64` | string | *biri zorunlu* | GLB dosyasının Base64 ile kodlanmış içeriği (URL yoksa) |
| `outputFileName` | string | Hayır | Çıktı USDZ dosya adı (uzantısız). Varsayılan: `output` |

`glbUrl` ve `glbBase64`’ten yalnızca biri verilmelidir.

## Çıktı (Output)

- **Key-Value Store:** `{outputFileName}.usdz` anahtarına binary USDZ dosyası yazılır. Run sonrası Apify konsolundan veya API ile indirilebilir.
- **Dataset:** Bir kayıt eklenir: `fileName`, `key`, `sizeBytes`, `message`.

## Apify’a Gönderme

1. [Apify Console](https://console.apify.com/) → Actors → Create new → **Empty actor** (veya “Build from Dockerfile”).
2. Bu repoyu bağlayın (Git push veya ZIP upload).
3. Root’ta `Dockerfile`, `main.py` ve `.actor/` klasörü olduğundan emin olun.
4. **Build** ile Docker image’ı oluşturun.
5. **Start** ile test edin; input’a örnek:

```json
{
  "glbUrl": "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/main/2.0/Duck/glTF-Binary/Duck.glb",
  "outputFileName": "duck"
}
```

## Yerel Çalıştırma (Docker)

Docker’da doğrudan `usd_from_gltf` kullanmak isterseniz:

```bash
docker run --rm -v %cd%:/app leon/usd-from-gltf:latest input.glb output.usdz
```

Bu actor ise Apify ortamında input (URL/base64) alıp çıktıyı Key-Value Store’a yazar.

## Notlar

- GLB dosyası geçerli glTF 2.0 (binary) olmalıdır.
- Çok büyük modeller veya karmaşık sahne yapıları dönüşüm süresini veya bellek kullanımını artırabilir.
- USDZ çıktısı AR Quick Look ile uyumludur; bazı glTF özellikleri emüle edilir veya sadeleştirilir (kaynak: [usd_from_gltf](https://github.com/google/usd_from_gltf)).

## Lisans

Actor kodu: MIT. Bağımlılıklar (Apify SDK, usd_from_gltf, USD) kendi lisanslarına tabidir.
