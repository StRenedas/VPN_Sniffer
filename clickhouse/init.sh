#!/bin/bash
set -e

clickhouse-client --user "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" -n <<-EOSQL
  CREATE TABLE VPN (
      id        UInt32 NOT NULL PRIMARY KEY,
      username  String,
      IP        IPv4,
      latitude  Float32,
      longitude Float32,
      time      String,
      date      Date32
  )
  ENGINE = MergeTree()
  ORDER BY id;

  CREATE TABLE ANOMALY (
      id       Int32,
      login_id Int32,
      username String
  )
  ENGINE = ReplacingMergeTree(id)
  ORDER BY login_id;
EOSQL