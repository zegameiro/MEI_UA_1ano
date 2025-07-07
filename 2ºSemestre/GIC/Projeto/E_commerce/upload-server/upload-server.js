// server.js
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const Minio = require('minio');

// MinIO client configuration
const minioClient = new Minio.Client({
  endPoint: process.env.MINIO_ENDPOINT,
  port: parseInt(process.env.MINIO_PORT, 10),
  useSSL: process.env.MINIO_USE_SSL,
  accessKey: process.env.MINIO_ACCESS_KEY,
  secretKey: process.env.MINIO_SECRET_KEY
});

const app = express();
const port = process.env.APP_PORT;
const bucket = process.env.MINIO_BUCKET;
const cdnBaseUrl = process.env.CDN_BASE_URL;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

async function ensureBucketExists() {
  try {
    const exists = await minioClient.bucketExists(bucket);
    if (!exists) {
      await minioClient.makeBucket(bucket);
      console.log(`Bucket '${bucket}' created.`);
    } else {
      console.log(`Bucket '${bucket}' already exists.`);
    }
  } catch (error) {
    console.error("Error ensuring bucket exists:", error);
  }
}

const upload = multer({
  storage: multer.memoryStorage()
});

app.post('/upload', upload.single('file'), async (req, res) => {
  if (!req.file) {
    return res.status(400).send('Ficheiro não encontrado.');
  }

  const objectName = req.file.originalname;
  const fileBuffer = req.file.buffer;
  const fileSize = req.file.size;
  const fileMimeType = req.file.mimetype;

  try {
    await minioClient.putObject(
      bucket,
      objectName,
      fileBuffer,
      fileSize,
      { 'Content-Type': fileMimeType }
    );
    console.log(`File '${objectName}' uploaded successfully to bucket '${bucket}'.`);

    const fullCdnUrl = `<span class="math-inline">${cdnBaseUrl}/</span>{objectName}`;
    res.json({ url: objectName, fullCdnUrl: fullCdnUrl });
  } catch (error) {
    console.error("Error uploading file to MinIO:", error);
    res.status(500).send('Erro no upload para MinIO.');
  }
});

// Start the server
app.listen(port, async () => {
  await ensureBucketExists();
  console.log(`Uploader ativo em http://upload.bytebazaar.k3s:${port}`);
});