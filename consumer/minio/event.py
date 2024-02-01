from typing import List, Any
from dataclasses import dataclass


@dataclass
class UserMetadata:
    content_type: str

    @staticmethod
    def from_dict(obj: Any) -> "UserMetadata":
        _content_type = str(obj.get("content-type"))
        return UserMetadata(_content_type)


@dataclass
class S3Object:
    key: str
    size: int
    e_tag: str
    content_type: str
    user_metadata: UserMetadata
    sequencer: str

    @staticmethod
    def from_dict(obj: Any) -> "S3Object":
        _key = str(obj.get("key"))
        _size = int(obj.get("size"))
        _e_tag = str(obj.get("eTag"))
        _content_type = str(obj.get("contentType"))
        _user_metadata = UserMetadata.from_dict(obj.get("userMetadata"))
        _sequencer = str(obj.get("sequencer"))
        return S3Object(_key, _size, _e_tag, _content_type, _user_metadata, _sequencer)


@dataclass
class OwnerIdentity:
    principal_id: str

    @staticmethod
    def from_dict(obj: Any) -> "OwnerIdentity":
        _principal_id = str(obj.get("principalId"))
        return OwnerIdentity(_principal_id)


@dataclass
class Bucket:
    name: str
    owner_identity: OwnerIdentity
    arn: str

    @staticmethod
    def from_dict(obj: Any) -> "Bucket":
        _name = str(obj.get("name"))
        _owner_identity = OwnerIdentity.from_dict(obj.get("ownerIdentity"))
        _arn = str(obj.get("arn"))
        return Bucket(_name, _owner_identity, _arn)


@dataclass
class S3:
    s3_schema_version: str
    configuration_id: str
    bucket: Bucket
    object: S3Object

    @staticmethod
    def from_dict(obj: Any) -> "S3":
        _s3_schema_version = str(obj.get("s3SchemaVersion"))
        _configuration_id = str(obj.get("configurationId"))
        _bucket = Bucket.from_dict(obj.get("bucket"))
        _object = S3Object.from_dict(obj.get("object"))
        return S3(_s3_schema_version, _configuration_id, _bucket, _object)


@dataclass
class ResponseElements:
    x_amz_id_2: str
    x_amz_request_id: str
    x_minio_deployment_id: str
    x_minio_origin_endpoint: str

    @staticmethod
    def from_dict(obj: Any) -> "ResponseElements":
        _x_amz_id_2 = str(obj.get("x-amz-id-2"))
        _x_amz_request_id = str(obj.get("x-amz-request-id"))
        _x_minio_deployment_id = str(obj.get("x-minio-deployment-id"))
        _x_minio_origin_endpoint = str(obj.get("x-minio-origin-endpoint"))
        return ResponseElements(
            _x_amz_id_2,
            _x_amz_request_id,
            _x_minio_deployment_id,
            _x_minio_origin_endpoint,
        )


@dataclass
class RequestParameters:
    principal_id: str
    region: str
    source_ip_address: str

    @staticmethod
    def from_dict(obj: Any) -> "RequestParameters":
        _principal_id = str(obj.get("principalId"))
        _region = str(obj.get("region"))
        _source_ip_address = str(obj.get("sourceIPAddress"))
        return RequestParameters(_principal_id, _region, _source_ip_address)


@dataclass
class UserIdentity:
    principal_id: str

    @staticmethod
    def from_dict(obj: Any) -> "UserIdentity":
        _principal_id = str(obj.get("principalId"))
        return UserIdentity(_principal_id)


@dataclass
class Source:
    host: str
    port: str
    user_agent: str

    @staticmethod
    def from_dict(obj: Any) -> "Source":
        _host = str(obj.get("host"))
        _port = str(obj.get("port"))
        _user_agent = str(obj.get("userAgent"))
        return Source(_host, _port, _user_agent)


@dataclass
class Record:
    event_version: str
    event_source: str
    aws_region: str
    event_time: str
    event_name: str
    user_identity: UserIdentity
    request_parameters: RequestParameters
    response_elements: ResponseElements
    s3: S3
    source: Source

    @staticmethod
    def from_dict(obj: Any) -> "Record":
        _event_version = str(obj.get("eventVersion"))
        _event_source = str(obj.get("eventSource"))
        _aws_region = str(obj.get("awsRegion"))
        _event_time = str(obj.get("eventTime"))
        _event_name = str(obj.get("eventName"))
        _user_identity = UserIdentity.from_dict(obj.get("userIdentity"))
        _request_parameters = RequestParameters.from_dict(obj.get("requestParameters"))
        _response_elements = ResponseElements.from_dict(obj.get("responseElements"))
        _s3 = S3.from_dict(obj.get("s3"))
        _source = Source.from_dict(obj.get("source"))
        return Record(
            _event_version,
            _event_source,
            _aws_region,
            _event_time,
            _event_name,
            _user_identity,
            _request_parameters,
            _response_elements,
            _s3,
            _source,
        )


@dataclass
class Event:
    event_name: str
    key: str
    records: List[Record]

    @staticmethod
    def from_dict(obj: Any) -> "Event":
        _event_name = str(obj.get("EventName"))
        _key = str(obj.get("Key"))
        _records = [Record.from_dict(y) for y in obj.get("Records")]
        return Event(_event_name, _key, _records)


# Example Usage
# json_string = json.loads(my_json_string)
# root = Event.from_dict(json_string)
