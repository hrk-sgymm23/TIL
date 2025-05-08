# Mountpoint for Amazon S3 CSI ドライバーを使用して Amazon S3 オブジェクトにアクセスする

https://docs.aws.amazon.com/ja_jp/eks/latest/userguide/s3-csi.html

## IAMポリシーを作成

```
{
   "Version": "2012-10-17",
   "Statement": [
        {
            "Sid": "MountpointFullBucketAccess",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::{バケット名}"
            ]
        },
        {
            "Sid": "MountpointFullObjectAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::{バケット名}/*"
            ]
        }
   ]
}
```
