# GLB to USDZ converter - uses Google's usd_from_gltf inside the image
FROM leon/usd-from-gltf:latest

# Override entrypoint so we run our Python actor, not usd_from_gltf directly
ENTRYPOINT []

# Install Apify SDK for Python
RUN pip install --no-cache-dir apify

WORKDIR /app
COPY main.py ./

CMD ["python", "main.py"]
