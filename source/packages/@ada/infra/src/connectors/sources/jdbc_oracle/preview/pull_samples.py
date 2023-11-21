###################################################################
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
###################################################################
import re
import awswrangler as wr
import os
import uuid

from handlers.common import *  # NOSONAR
from handlers.sampling.common import SamplingUtils  # NOSONAR
from handlers.sampling.common import PreviewGlueConnection  # NOSONAR
from handlers.sampling.common import SecretsManager  # NOSONAR
import pandas as pd

SOURCEDETAILS_CREDENTIAL_FIELD_NAME = 'password'
SOURCEDETAILS_CREDENTIAL_SECRET_NAME = 'dbCredentialSecretName'


def pull_samples(input: IPullSamplesInput) -> IPullSamplesReturn:  # NOSONAR (python:S3776) - false positive
    """
    Pull sample data from Oracle Database
    """
    boto3_session = input.boto3_session
    source_details = input.source_details
    sample_size = input.sample_size

    jdbc_connection_string = "jdbc:oracle:thin://@" + \
        source_details['databaseEndpoint'] + ":" + source_details['databasePort'] + "/" + source_details['databaseName']

    # retrieve password from source details
    db_password = SecretsManager.get_credentials_from_source( 
        source_details, 
        SOURCEDETAILS_CREDENTIAL_FIELD_NAME, 
        SOURCEDETAILS_CREDENTIAL_SECRET_NAME
    )

    with PreviewGlueConnection(jdbc_connection_string, source_details, db_password, boto3_session) as glue_connection_name:
        # aws wrangler to connect to oracle db and pull out a preview
        # sanitize sql table name to prevent sql injection
        table_name = source_details['databaseTable'].replace('`', '') 
        sql_query = f"SELECT * FROM {table_name} FETCH FIRST {str(sample_size)} rows only"

        try:
            df = None
            con_oracle = wr.oracle.connect(glue_connection_name, boto3_session=boto3_session)
            df = pd.DataFrame(wr.oracle.read_sql_query(sql=sql_query, con=con_oracle))
            con_oracle.close()
            
        except Exception as e:
            print(e)

    return [Sample(source_details['databaseTable'], next(iter([df])), 'parquet')]
