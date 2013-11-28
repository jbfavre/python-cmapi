# Licensed to Cloudera, Inc. under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  Cloudera, Inc. licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import random
import unittest
try:
  import json
except ImportError:
  import simplejson as json

from cm_api.endpoints.types import *
from cm_api.endpoints.services import ApiService
from cm_api_tests import utils

class TestReplicationTypes(unittest.TestCase):

  def test_hdfs_arguments(self):
    RAW = '''{
      "sourceService" : {
        "peerName" : "vst2",
        "clusterName" : "Cluster 1 - CDH4",
        "serviceName" : "HDFS-1"
      },
      "sourcePath" : "/data",
      "destinationPath" : "/copy/data2",
      "mapreduceServiceName" : "MAPREDUCE-1",
      "schedulerPoolName" : "medium",
      "userName" : "systest",
      "dryRun" : false,
      "abortOnError" : true,
      "removeMissingFiles" : false,
      "preserveReplicationCount" : true,
      "preserveBlockSize" : true,
      "preservePermissions" : false
    }'''
    args = utils.deserialize(RAW, ApiHdfsReplicationArguments)
    self.assertEquals('vst2', args.sourceService.peerName)
    self.assertEquals('Cluster 1 - CDH4', args.sourceService.clusterName)
    self.assertEquals('HDFS-1', args.sourceService.serviceName)
    self.assertEquals('/data', args.sourcePath)
    self.assertEquals('/copy/data2', args.destinationPath)
    self.assertEquals('MAPREDUCE-1', args.mapreduceServiceName)
    self.assertEquals('medium', args.schedulerPoolName)
    self.assertEquals('systest', args.userName)
    self.assertFalse(args.dryRun)
    self.assertTrue(args.abortOnError)
    self.assertFalse(args.removeMissingFiles)
    self.assertTrue(args.preserveBlockSize)
    self.assertFalse(args.preservePermissions)
    self.assertTrue(args.preserveReplicationCount)

  def test_hive_arguments(self):
    RAW = '''{
      "sourceService" : {
        "peerName" : "vst2",
        "clusterName" : "Cluster 1 - CDH4",
        "serviceName" : "HIVE-1"
      },
      "force" : true,
      "replicateData" : true,
      "hdfsArguments" : {
        "mapreduceServiceName" : "MAPREDUCE-1",
        "dryRun" : false,
        "abortOnError" : false,
        "removeMissingFiles" : false,
        "preserveReplicationCount" : false,
        "preserveBlockSize" : false,
        "preservePermissions" : false
      },
      "tableFilters" : [
        { "database" : "db1", "tableName" : "table1" }
      ],
      "dryRun" : false
    }'''
    args = utils.deserialize(RAW, ApiHiveReplicationArguments)
    self.assertEquals('vst2', args.sourceService.peerName)
    self.assertEquals('Cluster 1 - CDH4', args.sourceService.clusterName)
    self.assertEquals('HIVE-1', args.sourceService.serviceName)
    self.assertTrue(args.force)
    self.assertTrue(args.replicateData)
    self.assertIsInstance(args.hdfsArguments, ApiHdfsReplicationArguments)
    self.assertIsInstance(args.tableFilters, list)
    self.assertEquals(1, len(args.tableFilters))
    self.assertIsInstance(args.tableFilters[0], ApiHiveTable)
    self.assertEquals("db1", args.tableFilters[0].database)
    self.assertEquals("table1", args.tableFilters[0].tableName)

  def test_schedule(self):
    RAW = '''{
      "id" : 39,
      "startTime" : "2012-12-10T23:11:31.041Z",
      "interval" : 1,
      "intervalUnit" : "DAY",
      "paused" : false,
      "nextRun" : "2013-01-15T23:11:31.041Z",
      "history" : [ {
        "id" : 738,
        "name" : "HiveReplicationCommand",
        "startTime" : "2013-01-15T18:28:24.895Z",
        "endTime" : "2013-01-15T18:30:49.446Z",
        "active" : false,
        "success" : true,
        "resultMessage" : "Hive Replication Finished Successfully.",
        "resultDataUrl" : "/cmf/command/738/download",
        "serviceRef" : {
          "clusterName" : "Cluster 1 - CDH4",
          "serviceName" : "HIVE-1"
        },
        "hiveResult" : {
          "tables" : [ {
            "database" : "default",
            "tableName" : "repl_test_1"
          }, {
            "database" : "default",
            "tableName" : "sample_07"
          }, {
            "database" : "default",
            "tableName" : "sample_08"
          } ],
          "errors" : [ ],
          "dataReplicationResult" : {
            "progress" : 100,
            "numFilesCopied" : 0,
            "numBytesCopied" : 0,
            "numFilesSkipped" : 3,
            "numBytesSkipped" : 92158,
            "numFilesDeleted" : 0,
            "numFilesCopyFailed" : 0,
            "numBytesCopyFailed" : 0,
            "dryRun" : false
          },
          "dryRun" : false
        }
      } ],
      "alertOnStart" : false,
      "alertOnSuccess" : false,
      "alertOnFail" : false,
      "alertOnAbort" : false,
      "hiveArguments" : {
        "sourceService" : {
          "peerName" : "vst2",
          "clusterName" : "Cluster 1 - CDH4",
          "serviceName" : "HIVE-1"
        },
        "force" : true,
        "replicateData" : true,
        "hdfsArguments" : {
          "mapreduceServiceName" : "MAPREDUCE-1",
          "dryRun" : false,
          "abortOnError" : false,
          "removeMissingFiles" : false,
          "preserveReplicationCount" : false,
          "preserveBlockSize" : false,
          "preservePermissions" : false
        },
        "dryRun" : false
      }
    }'''
    sched = utils.deserialize(RAW, ApiReplicationSchedule)
    self.assertEqual(39, sched.id)
    self.assertEqual(self._parse_time("2012-12-10T23:11:31.041Z"), sched.startTime)
    self.assertEqual('DAY', sched.intervalUnit)
    self.assertEqual(1, sched.interval)
    self.assertFalse(sched.paused)
    self.assertEqual(self._parse_time("2013-01-15T23:11:31.041Z"), sched.nextRun)
    self.assertFalse(sched.alertOnStart)
    self.assertIsNotNone(sched.hiveArguments)

    self.assertEqual(1, len(sched.history))
    self.assertIsInstance(sched.history[0], ApiReplicationCommand)
    self.assertEqual('default', sched.history[0].hiveResult.tables[0].database)
    self.assertEqual(92158, sched.history[0].hiveResult.dataReplicationResult.numBytesSkipped)

  def test_peers(self):
    RAW = '''{
      "name" : "peer1",
      "url" : "http://peer1",
      "username" : "user1",
      "password" : "pwd"
    }'''
    peer = ApiCmPeer.from_json_dict(json.loads(RAW), None)
    self.assertEquals("peer1", peer.name)
    self.assertEquals("http://peer1", peer.url)
    self.assertEquals("user1", peer.username)
    self.assertEquals("pwd", peer.password)

  def _parse_time(self, tstr):
    return datetime.datetime.strptime(tstr, "%Y-%m-%dT%H:%M:%S.%fZ")


class TestReplicationRequests(unittest.TestCase):

  def __init__(self, methodName):
    super(TestReplicationRequests, self).__init__(methodName)
    self.resource = utils.MockResource(self)

  def test_replication_crud(self):
    service = ApiService(self.resource, 'hdfs1', 'HDFS')
    service.__dict__['clusterRef'] = ApiClusterRef(self.resource, clusterName='cluster1')

    hdfs_args = ApiHdfsReplicationArguments(self.resource)
    hdfs_args.sourceService = ApiServiceRef('cluster2', 'hdfs2')
    hdfs_args.sourcePath = '/src'
    hdfs_args.destinationPath = '/dst'

    return_sched = ApiReplicationSchedule(self.resource,
        interval=2, intervalUnit='DAY')
    return_sched.hdfsArguments = hdfs_args
    return_sched.__dict__['id'] = 1
    return_list = ApiList([ return_sched ]).to_json_dict()

    self.resource.expect("POST",
        "/clusters/cluster1/services/hdfs1/replications",
        retdata=return_list)

    sched = service.create_replication_schedule(
        None, None, 'DAY', 2, True, hdfs_args, alert_on_fail=True)
    self.assertEqual(return_sched.intervalUnit, sched.intervalUnit)
    self.assertEqual(return_sched.interval, sched.interval)
    self.assertIsInstance(sched.hdfsArguments, ApiHdfsReplicationArguments)

    self.resource.expect("GET",
        "/clusters/cluster1/services/hdfs1/replications",
        retdata=return_list)
    service.get_replication_schedules()

    self.resource.expect("GET",
        "/clusters/cluster1/services/hdfs1/replications/1",
        retdata=return_sched.to_json_dict())
    service.get_replication_schedule(1)

    self.resource.expect("PUT",
        "/clusters/cluster1/services/hdfs1/replications/1",
        retdata=return_sched.to_json_dict())
    service.update_replication_schedule(1, return_sched)

    self.resource.expect("DELETE",
        "/clusters/cluster1/services/hdfs1/replications/1",
        retdata=return_sched.to_json_dict())
    service.delete_replication_schedule(1)

if __name__ == '__main__':
    unittest.main()
