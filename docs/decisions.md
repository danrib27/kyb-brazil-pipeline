# Architecture Decision Records

## ADR-001: Replace staging/archive tables with Iceberg and partition-aware orchestration

- **Status:** Accepted
- **Date:** 2026-11-01

### Context

A common pattern in Hive-based data lakes processes each batch in four steps:
ingest raw files, load them into a temporary Hive external table, transform
with dbt, then move the temporary data into an archive table to record what has
been processed.

The staging and archive tables exist because Hive tables have no
transactions, no history and no notion of which data was already processed.
Batch tracking has to be implemented by hand.

### Decision

Use a three-step flow instead:

1. **Ingestion:** store original files, immutable, in the `raw/` zone on S3.
2. **Bronze:** load each raw partition into a permanent Apache Iceberg table,
   overwriting the partition on reprocessing and adding audit columns
   (`_ingested_at`, `_source_file`, `_batch_id`).
3. **dbt:** incremental models read new data from bronze and build facts and
   dimensions.

Processed-batch tracking comes from Dagster's per-partition materialization
history, row-level lineage from the audit columns, and rollback from Iceberg
snapshots.

### Alternatives considered

- **Staging + archive tables (Hive pattern):** proven, but adds an extra step
  and custom code to maintain for guarantees the table format now provides.
- **Delta Lake instead of Iceberg:** similar capabilities; Iceberg chosen for
  its engine-agnostic design and native support in AWS Glue and Athena.

### Consequences

- ✅ Fewer pipeline steps and less custom code.
- ✅ Idempotent reprocessing: rerunning a partition overwrites it.
- ✅ Trivial backfills through Dagster partitions.
- ✅ Point-in-time queries via Iceberg time travel.
- ⚠️ Requires understanding Iceberg snapshot management (expiring old
  snapshots to control storage costs).
