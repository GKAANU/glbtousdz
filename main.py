"""
Apify Actor: GLB to USDZ Converter
Converts GLB 3D AR models to Apple USDZ format using usd_from_gltf.
"""
import os
import base64
import tempfile
import subprocess

from apify import Actor

CONVERTER_BIN = "usd_from_gltf"


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        glb_url = actor_input.get("glbUrl", "").strip()
        glb_base64 = actor_input.get("glbBase64", "").strip()
        output_name = (actor_input.get("outputFileName") or "output").strip() or "output"
        if output_name.lower().endswith(".usdz"):
            output_name = output_name[:-5]

        if not glb_url and not glb_base64:
            await Actor.fail(
                "Either 'glbUrl' or 'glbBase64' must be provided in the input."
            )
        if glb_url and glb_base64:
            await Actor.fail(
                "Provide only one of 'glbUrl' or 'glbBase64', not both."
            )

        with tempfile.TemporaryDirectory(prefix="glb2usdz_") as tmpdir:
            glb_path = os.path.join(tmpdir, "input.glb")

            if glb_url:
                Actor.log.info(f"Downloading GLB from: {glb_url}")
                try:
                    import urllib.request
                    urllib.request.urlretrieve(glb_url, glb_path)
                except Exception as e:
                    await Actor.fail(f"Failed to download GLB from URL: {e}")
            else:
                Actor.log.info("Decoding base64 GLB data...")
                try:
                    data = base64.b64decode(glb_base64, validate=True)
                    with open(glb_path, "wb") as f:
                        f.write(data)
                except Exception as e:
                    await Actor.fail(f"Invalid base64 GLB data: {e}")

            if not os.path.isfile(glb_path) or os.path.getsize(glb_path) == 0:
                await Actor.fail("GLB file is empty or could not be written.")

            usdz_path = os.path.join(tmpdir, f"{output_name}.usdz")
            Actor.log.info("Converting GLB to USDZ...")

            try:
                result = subprocess.run(
                    [CONVERTER_BIN, glb_path, usdz_path],
                    capture_output=True,
                    text=True,
                    timeout=300,
                    env=os.environ.copy(),
                    cwd=tmpdir,
                )
            except subprocess.TimeoutExpired:
                await Actor.fail("Conversion timed out after 5 minutes.")
            except FileNotFoundError:
                await Actor.fail(
                    f"Converter '{CONVERTER_BIN}' not found. Ensure the actor uses the correct Docker image."
                )

            if result.returncode != 0:
                err = (result.stderr or result.stdout or "").strip()
                await Actor.fail(f"Conversion failed: {err or f'exit code {result.returncode}'}")

            if not os.path.isfile(usdz_path):
                await Actor.fail("Conversion did not produce an output USDZ file.")

            with open(usdz_path, "rb") as f:
                usdz_data = f.read()

            output_key = f"{output_name}.usdz"
            await Actor.set_value(output_key, usdz_data, content_type="model/vnd.usdz+zip")

            await Actor.push_data({
                "fileName": output_key,
                "key": output_key,
                "sizeBytes": len(usdz_data),
                "message": "Converted successfully. Download from Actor run key-value store.",
            })

            Actor.log.info(f"Conversion done. Output: {output_key} ({len(usdz_data)} bytes)")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
