
import boto3
import logger
from botocore.exceptions import ClientError


class BucketWrapper:
    def create_versioned_bucket(bucket_name, prefix=None):
        """
        Creates an Amazon S3 bucket, enables it for versioning, and configures a lifecycle
        that expires noncurrent object versions after 7 days.

        Adding a lifecycle configuration to a versioned bucket is a best practice.
        It helps prevent objects in the bucket from accumulating a large number of
        noncurrent versions, which can slow down request performance.

        Usage is shown in the usage_demo_single_object function at the end of this module.

        :param bucket_name: The name of the bucket to create.
        :param prefix: Identifies which objects are automatically expired under the
                    configured lifecycle rules.
        :return: The newly created bucket.
        """
        try:
            s3 = boto3.client('s3')
            bucket = s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": s3.meta.client.meta.region_name
                },
            )
            logger.info("Created bucket %s.", bucket.name)
        except ClientError as error:
            if error.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
                logger.warning("Bucket %s already exists! Using it.", bucket_name)
                bucket = s3.Bucket(bucket_name)
            else:
                logger.exception("Couldn't create bucket %s.", bucket_name)
                raise

        try:
            bucket.Versioning().enable()
            logger.info("Enabled versioning on bucket %s.", bucket.name)
        except ClientError:
            logger.exception("Couldn't enable versioning on bucket %s.", bucket.name)
            raise

        try:
            expiration = 7
            bucket.LifecycleConfiguration().put(
                LifecycleConfiguration={
                    "Rules": [
                        {
                            "Status": "Enabled",
                            "Prefix": prefix,
                            "NoncurrentVersionExpiration": {"NoncurrentDays": expiration},
                        }
                    ]
                }
            )
            logger.info(
                "Configured lifecycle to expire noncurrent versions after %s days "
                "on bucket %s.",
                expiration,
                bucket.name,
            )
        except ClientError as error:
            logger.warning(
                "Couldn't configure lifecycle on bucket %s because %s. "
                "Continuing anyway.",
                bucket.name,
                error,
            )

        return bucket



