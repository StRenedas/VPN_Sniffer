#!/bin/bash
set -e

clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" -n <<-EOSQL
  CREATE TABLE VPN (
      id        UUID NOT NULL PRIMARY KEY,
      username  String,
      IP        IPv4,
      latitude  Float32,
      longitude Float32,
      datetime  DateTime
  )
  ENGINE = MergeTree()
  ORDER BY id;

  CREATE TABLE ANOMALY (
      id       UUID,
      login_id UUID,
      username String
  )
  ENGINE = MergeTree
  ORDER BY login_id;
EOSQL