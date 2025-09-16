CREATE VECTOR INDEX `${GCP_PROJECT}.${BQ_DATASET}.idx_stitched`
ON `${GCP_PROJECT}.${BQ_DATASET}.emb_stitched`(vec)
OPTIONS(distance_type='COSINE');

