# flake8: noqa
# fmt: off
import json
import os.path
import decimal
import datetime
import six
from avrogen.dict_wrapper import DictWrapper
from avrogen import avrojson
from avro.schema import RecordSchema, SchemaFromJSONData as make_avsc_object
from avro import schema as avro_schema
from typing import List, Dict, Union, Optional


def __read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()
        

def __get_names_and_schema(json_str):
    names = avro_schema.Names()
    schema = make_avsc_object(json.loads(json_str), names)
    return names, schema


SCHEMA_JSON_STR = __read_file(os.path.join(os.path.dirname(__file__), "schema.avsc"))


__NAMES, SCHEMA = __get_names_and_schema(SCHEMA_JSON_STR)
__SCHEMAS: Dict[str, RecordSchema] = {}


def get_schema_type(fullname):
    return __SCHEMAS.get(fullname)
    
    
__SCHEMAS = dict((n.fullname.lstrip("."), n) for n in six.itervalues(__NAMES.names))

class KafkaAuditHeaderClass(DictWrapper):
    """This header records information about the context of an event as it is emitted into kafka and is intended to be used by the kafka audit application.  For more information see go/kafkaauditheader"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.events.KafkaAuditHeader")
    def __init__(self,
        time: int,
        server: str,
        appName: str,
        messageId: bytes,
        instance: Union[None, str]=None,
        auditVersion: Union[None, int]=None,
        fabricUrn: Union[None, str]=None,
        clusterConnectionString: Union[None, str]=None,
    ):
        super().__init__()
        
        self.time = time
        self.server = server
        self.instance = instance
        self.appName = appName
        self.messageId = messageId
        self.auditVersion = auditVersion
        self.fabricUrn = fabricUrn
        self.clusterConnectionString = clusterConnectionString
    
    @classmethod
    def construct_with_defaults(cls) -> "KafkaAuditHeaderClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.time = int()
        self.server = str()
        self.instance = self.RECORD_SCHEMA.field_map["instance"].default
        self.appName = str()
        self.messageId = bytes()
        self.auditVersion = self.RECORD_SCHEMA.field_map["auditVersion"].default
        self.fabricUrn = self.RECORD_SCHEMA.field_map["fabricUrn"].default
        self.clusterConnectionString = self.RECORD_SCHEMA.field_map["clusterConnectionString"].default
    
    
    @property
    def time(self) -> int:
        """Getter: The time at which the event was emitted into kafka."""
        return self._inner_dict.get('time')  # type: ignore
    
    
    @time.setter
    def time(self, value: int) -> None:
        """Setter: The time at which the event was emitted into kafka."""
        self._inner_dict['time'] = value
    
    
    @property
    def server(self) -> str:
        """Getter: The fully qualified name of the host from which the event is being emitted."""
        return self._inner_dict.get('server')  # type: ignore
    
    
    @server.setter
    def server(self, value: str) -> None:
        """Setter: The fully qualified name of the host from which the event is being emitted."""
        self._inner_dict['server'] = value
    
    
    @property
    def instance(self) -> Union[None, str]:
        """Getter: The instance on the server from which the event is being emitted. e.g. i001"""
        return self._inner_dict.get('instance')  # type: ignore
    
    
    @instance.setter
    def instance(self, value: Union[None, str]) -> None:
        """Setter: The instance on the server from which the event is being emitted. e.g. i001"""
        self._inner_dict['instance'] = value
    
    
    @property
    def appName(self) -> str:
        """Getter: The name of the application from which the event is being emitted. see go/appname"""
        return self._inner_dict.get('appName')  # type: ignore
    
    
    @appName.setter
    def appName(self, value: str) -> None:
        """Setter: The name of the application from which the event is being emitted. see go/appname"""
        self._inner_dict['appName'] = value
    
    
    @property
    def messageId(self) -> bytes:
        """Getter: A unique identifier for the message"""
        return self._inner_dict.get('messageId')  # type: ignore
    
    
    @messageId.setter
    def messageId(self, value: bytes) -> None:
        """Setter: A unique identifier for the message"""
        self._inner_dict['messageId'] = value
    
    
    @property
    def auditVersion(self) -> Union[None, int]:
        """Getter: The version that is being used for auditing. In version 0, the audit trail buckets events into 10 minute audit windows based on the EventHeader timestamp. In version 1, the audit trail buckets events as follows: if the schema has an outer KafkaAuditHeader, use the outer audit header timestamp for bucketing; else if the EventHeader has an inner KafkaAuditHeader use that inner audit header's timestamp for bucketing"""
        return self._inner_dict.get('auditVersion')  # type: ignore
    
    
    @auditVersion.setter
    def auditVersion(self, value: Union[None, int]) -> None:
        """Setter: The version that is being used for auditing. In version 0, the audit trail buckets events into 10 minute audit windows based on the EventHeader timestamp. In version 1, the audit trail buckets events as follows: if the schema has an outer KafkaAuditHeader, use the outer audit header timestamp for bucketing; else if the EventHeader has an inner KafkaAuditHeader use that inner audit header's timestamp for bucketing"""
        self._inner_dict['auditVersion'] = value
    
    
    @property
    def fabricUrn(self) -> Union[None, str]:
        """Getter: The fabricUrn of the host from which the event is being emitted. Fabric Urn in the format of urn:li:fabric:{fabric_name}. See go/fabric."""
        return self._inner_dict.get('fabricUrn')  # type: ignore
    
    
    @fabricUrn.setter
    def fabricUrn(self, value: Union[None, str]) -> None:
        """Setter: The fabricUrn of the host from which the event is being emitted. Fabric Urn in the format of urn:li:fabric:{fabric_name}. See go/fabric."""
        self._inner_dict['fabricUrn'] = value
    
    
    @property
    def clusterConnectionString(self) -> Union[None, str]:
        """Getter: This is a String that the client uses to establish some kind of connection with the Kafka cluster. The exact format of it depends on specific versions of clients and brokers. This information could potentially identify the fabric and cluster with which the client is producing to or consuming from."""
        return self._inner_dict.get('clusterConnectionString')  # type: ignore
    
    
    @clusterConnectionString.setter
    def clusterConnectionString(self, value: Union[None, str]) -> None:
        """Setter: This is a String that the client uses to establish some kind of connection with the Kafka cluster. The exact format of it depends on specific versions of clients and brokers. This information could potentially identify the fabric and cluster with which the client is producing to or consuming from."""
        self._inner_dict['clusterConnectionString'] = value
    
    
class ChartInfoClass(DictWrapper):
    """Information about a chart"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.chart.ChartInfo")
    def __init__(self,
        title: str,
        description: str,
        lastModified: "ChangeAuditStampsClass",
        customProperties: Optional[Dict[str, str]]=None,
        externalUrl: Union[None, str]=None,
        chartUrl: Union[None, str]=None,
        inputs: Union[None, List[str]]=None,
        type: Union[None, Union[str, "ChartTypeClass"]]=None,
        access: Union[None, Union[str, "AccessLevelClass"]]=None,
        lastRefreshed: Union[None, int]=None,
    ):
        super().__init__()
        
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
        self.externalUrl = externalUrl
        self.title = title
        self.description = description
        self.lastModified = lastModified
        self.chartUrl = chartUrl
        self.inputs = inputs
        self.type = type
        self.access = access
        self.lastRefreshed = lastRefreshed
    
    @classmethod
    def construct_with_defaults(cls) -> "ChartInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.customProperties = dict()
        self.externalUrl = self.RECORD_SCHEMA.field_map["externalUrl"].default
        self.title = str()
        self.description = str()
        self.lastModified = ChangeAuditStampsClass.construct_with_defaults()
        self.chartUrl = self.RECORD_SCHEMA.field_map["chartUrl"].default
        self.inputs = self.RECORD_SCHEMA.field_map["inputs"].default
        self.type = self.RECORD_SCHEMA.field_map["type"].default
        self.access = self.RECORD_SCHEMA.field_map["access"].default
        self.lastRefreshed = self.RECORD_SCHEMA.field_map["lastRefreshed"].default
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: Custom property bag."""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: Custom property bag."""
        self._inner_dict['customProperties'] = value
    
    
    @property
    def externalUrl(self) -> Union[None, str]:
        """Getter: URL where the reference exist"""
        return self._inner_dict.get('externalUrl')  # type: ignore
    
    
    @externalUrl.setter
    def externalUrl(self, value: Union[None, str]) -> None:
        """Setter: URL where the reference exist"""
        self._inner_dict['externalUrl'] = value
    
    
    @property
    def title(self) -> str:
        """Getter: Title of the chart"""
        return self._inner_dict.get('title')  # type: ignore
    
    
    @title.setter
    def title(self, value: str) -> None:
        """Setter: Title of the chart"""
        self._inner_dict['title'] = value
    
    
    @property
    def description(self) -> str:
        """Getter: Detailed description about the chart"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: str) -> None:
        """Setter: Detailed description about the chart"""
        self._inner_dict['description'] = value
    
    
    @property
    def lastModified(self) -> "ChangeAuditStampsClass":
        """Getter: Captures information about who created/last modified/deleted this chart and when"""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "ChangeAuditStampsClass") -> None:
        """Setter: Captures information about who created/last modified/deleted this chart and when"""
        self._inner_dict['lastModified'] = value
    
    
    @property
    def chartUrl(self) -> Union[None, str]:
        """Getter: URL for the chart. This could be used as an external link on DataHub to allow users access/view the chart"""
        return self._inner_dict.get('chartUrl')  # type: ignore
    
    
    @chartUrl.setter
    def chartUrl(self, value: Union[None, str]) -> None:
        """Setter: URL for the chart. This could be used as an external link on DataHub to allow users access/view the chart"""
        self._inner_dict['chartUrl'] = value
    
    
    @property
    def inputs(self) -> Union[None, List[str]]:
        """Getter: Data sources for the chart"""
        return self._inner_dict.get('inputs')  # type: ignore
    
    
    @inputs.setter
    def inputs(self, value: Union[None, List[str]]) -> None:
        """Setter: Data sources for the chart"""
        self._inner_dict['inputs'] = value
    
    
    @property
    def type(self) -> Union[None, Union[str, "ChartTypeClass"]]:
        """Getter: Type of the chart"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[None, Union[str, "ChartTypeClass"]]) -> None:
        """Setter: Type of the chart"""
        self._inner_dict['type'] = value
    
    
    @property
    def access(self) -> Union[None, Union[str, "AccessLevelClass"]]:
        """Getter: Access level for the chart"""
        return self._inner_dict.get('access')  # type: ignore
    
    
    @access.setter
    def access(self, value: Union[None, Union[str, "AccessLevelClass"]]) -> None:
        """Setter: Access level for the chart"""
        self._inner_dict['access'] = value
    
    
    @property
    def lastRefreshed(self) -> Union[None, int]:
        """Getter: The time when this chart last refreshed"""
        return self._inner_dict.get('lastRefreshed')  # type: ignore
    
    
    @lastRefreshed.setter
    def lastRefreshed(self, value: Union[None, int]) -> None:
        """Setter: The time when this chart last refreshed"""
        self._inner_dict['lastRefreshed'] = value
    
    
class ChartQueryClass(DictWrapper):
    """Information for chart query which is used for getting data of the chart"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.chart.ChartQuery")
    def __init__(self,
        rawQuery: str,
        type: Union[str, "ChartQueryTypeClass"],
    ):
        super().__init__()
        
        self.rawQuery = rawQuery
        self.type = type
    
    @classmethod
    def construct_with_defaults(cls) -> "ChartQueryClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.rawQuery = str()
        self.type = ChartQueryTypeClass.LOOKML
    
    
    @property
    def rawQuery(self) -> str:
        """Getter: Raw query to build a chart from input datasets"""
        return self._inner_dict.get('rawQuery')  # type: ignore
    
    
    @rawQuery.setter
    def rawQuery(self, value: str) -> None:
        """Setter: Raw query to build a chart from input datasets"""
        self._inner_dict['rawQuery'] = value
    
    
    @property
    def type(self) -> Union[str, "ChartQueryTypeClass"]:
        """Getter: Chart query type"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "ChartQueryTypeClass"]) -> None:
        """Setter: Chart query type"""
        self._inner_dict['type'] = value
    
    
class ChartQueryTypeClass(object):
    # No docs available.
    
    
    """LookML queries"""
    LOOKML = "LOOKML"
    
    """SQL type queries"""
    SQL = "SQL"
    
    
class ChartTypeClass(object):
    """The various types of charts"""
    
    
    """Chart showing a Bar chart"""
    BAR = "BAR"
    
    """Chart showing a Pie chart"""
    PIE = "PIE"
    
    """Chart showing a Scatter plot"""
    SCATTER = "SCATTER"
    
    """Chart showing a table"""
    TABLE = "TABLE"
    
    """Chart showing Markdown formatted text"""
    TEXT = "TEXT"
    
    LINE = "LINE"
    
    AREA = "AREA"
    
    HISTOGRAM = "HISTOGRAM"
    
    BOX_PLOT = "BOX_PLOT"
    
    
class AccessLevelClass(object):
    """The various access levels"""
    
    
    """Publicly available access level"""
    PUBLIC = "PUBLIC"
    
    """Private availability to certain set of users"""
    PRIVATE = "PRIVATE"
    
    
class AuditStampClass(DictWrapper):
    """Data captured on a resource/association/sub-resource level giving insight into when that resource/association/sub-resource moved into a particular lifecycle stage, and who acted to move it into that specific lifecycle stage."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.AuditStamp")
    def __init__(self,
        time: int,
        actor: str,
        impersonator: Union[None, str]=None,
    ):
        super().__init__()
        
        self.time = time
        self.actor = actor
        self.impersonator = impersonator
    
    @classmethod
    def construct_with_defaults(cls) -> "AuditStampClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.time = int()
        self.actor = str()
        self.impersonator = self.RECORD_SCHEMA.field_map["impersonator"].default
    
    
    @property
    def time(self) -> int:
        """Getter: When did the resource/association/sub-resource move into the specific lifecycle stage represented by this AuditEvent."""
        return self._inner_dict.get('time')  # type: ignore
    
    
    @time.setter
    def time(self, value: int) -> None:
        """Setter: When did the resource/association/sub-resource move into the specific lifecycle stage represented by this AuditEvent."""
        self._inner_dict['time'] = value
    
    
    @property
    def actor(self) -> str:
        """Getter: The entity (e.g. a member URN) which will be credited for moving the resource/association/sub-resource into the specific lifecycle stage. It is also the one used to authorize the change."""
        return self._inner_dict.get('actor')  # type: ignore
    
    
    @actor.setter
    def actor(self, value: str) -> None:
        """Setter: The entity (e.g. a member URN) which will be credited for moving the resource/association/sub-resource into the specific lifecycle stage. It is also the one used to authorize the change."""
        self._inner_dict['actor'] = value
    
    
    @property
    def impersonator(self) -> Union[None, str]:
        """Getter: The entity (e.g. a service URN) which performs the change on behalf of the Actor and must be authorized to act as the Actor."""
        return self._inner_dict.get('impersonator')  # type: ignore
    
    
    @impersonator.setter
    def impersonator(self, value: Union[None, str]) -> None:
        """Setter: The entity (e.g. a service URN) which performs the change on behalf of the Actor and must be authorized to act as the Actor."""
        self._inner_dict['impersonator'] = value
    
    
class ChangeAuditStampsClass(DictWrapper):
    """Data captured on a resource/association/sub-resource level giving insight into when that resource/association/sub-resource moved into various lifecycle stages, and who acted to move it into those lifecycle stages. The recommended best practice is to include this record in your record schema, and annotate its fields as @readOnly in your resource. See https://github.com/linkedin/rest.li/wiki/Validation-in-Rest.li#restli-validation-annotations"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.ChangeAuditStamps")
    def __init__(self,
        created: "AuditStampClass",
        lastModified: "AuditStampClass",
        deleted: Union[None, "AuditStampClass"]=None,
    ):
        super().__init__()
        
        self.created = created
        self.lastModified = lastModified
        self.deleted = deleted
    
    @classmethod
    def construct_with_defaults(cls) -> "ChangeAuditStampsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.created = AuditStampClass.construct_with_defaults()
        self.lastModified = AuditStampClass.construct_with_defaults()
        self.deleted = self.RECORD_SCHEMA.field_map["deleted"].default
    
    
    @property
    def created(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        return self._inner_dict.get('created')  # type: ignore
    
    
    @created.setter
    def created(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        self._inner_dict['created'] = value
    
    
    @property
    def lastModified(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        self._inner_dict['lastModified'] = value
    
    
    @property
    def deleted(self) -> Union[None, "AuditStampClass"]:
        """Getter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        return self._inner_dict.get('deleted')  # type: ignore
    
    
    @deleted.setter
    def deleted(self, value: Union[None, "AuditStampClass"]) -> None:
        """Setter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        self._inner_dict['deleted'] = value
    
    
class CostClass(DictWrapper):
    # No docs available.
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.Cost")
    def __init__(self,
        costType: Union[str, "CostTypeClass"],
        cost: "CostCostClass",
    ):
        super().__init__()
        
        self.costType = costType
        self.cost = cost
    
    @classmethod
    def construct_with_defaults(cls) -> "CostClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.costType = CostTypeClass.ORG_COST_TYPE
        self.cost = CostCostClass.construct_with_defaults()
    
    
    @property
    def costType(self) -> Union[str, "CostTypeClass"]:
        # No docs available.
        return self._inner_dict.get('costType')  # type: ignore
    
    
    @costType.setter
    def costType(self, value: Union[str, "CostTypeClass"]) -> None:
        # No docs available.
        self._inner_dict['costType'] = value
    
    
    @property
    def cost(self) -> "CostCostClass":
        # No docs available.
        return self._inner_dict.get('cost')  # type: ignore
    
    
    @cost.setter
    def cost(self, value: "CostCostClass") -> None:
        # No docs available.
        self._inner_dict['cost'] = value
    
    
class CostCostClass(DictWrapper):
    # No docs available.
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.CostCost")
    def __init__(self,
        fieldDiscriminator: Union[str, "CostCostDiscriminatorClass"],
        costId: Union[None, float]=None,
        costCode: Union[None, str]=None,
    ):
        super().__init__()
        
        self.costId = costId
        self.costCode = costCode
        self.fieldDiscriminator = fieldDiscriminator
    
    @classmethod
    def construct_with_defaults(cls) -> "CostCostClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.costId = self.RECORD_SCHEMA.field_map["costId"].default
        self.costCode = self.RECORD_SCHEMA.field_map["costCode"].default
        self.fieldDiscriminator = CostCostDiscriminatorClass.costId
    
    
    @property
    def costId(self) -> Union[None, float]:
        # No docs available.
        return self._inner_dict.get('costId')  # type: ignore
    
    
    @costId.setter
    def costId(self, value: Union[None, float]) -> None:
        # No docs available.
        self._inner_dict['costId'] = value
    
    
    @property
    def costCode(self) -> Union[None, str]:
        # No docs available.
        return self._inner_dict.get('costCode')  # type: ignore
    
    
    @costCode.setter
    def costCode(self, value: Union[None, str]) -> None:
        # No docs available.
        self._inner_dict['costCode'] = value
    
    
    @property
    def fieldDiscriminator(self) -> Union[str, "CostCostDiscriminatorClass"]:
        """Getter: Contains the name of the field that has its value set."""
        return self._inner_dict.get('fieldDiscriminator')  # type: ignore
    
    
    @fieldDiscriminator.setter
    def fieldDiscriminator(self, value: Union[str, "CostCostDiscriminatorClass"]) -> None:
        """Setter: Contains the name of the field that has its value set."""
        self._inner_dict['fieldDiscriminator'] = value
    
    
class CostCostDiscriminatorClass(object):
    # No docs available.
    
    costId = "costId"
    costCode = "costCode"
    
    
class CostTypeClass(object):
    """Type of Cost Code"""
    
    
    """Org Cost Type to which the Cost of this entity should be attributed to"""
    ORG_COST_TYPE = "ORG_COST_TYPE"
    
    
class DeprecationClass(DictWrapper):
    """Deprecation status of an entity"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.Deprecation")
    def __init__(self,
        deprecated: bool,
        note: str,
        actor: str,
        decommissionTime: Union[None, int]=None,
    ):
        super().__init__()
        
        self.deprecated = deprecated
        self.decommissionTime = decommissionTime
        self.note = note
        self.actor = actor
    
    @classmethod
    def construct_with_defaults(cls) -> "DeprecationClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.deprecated = bool()
        self.decommissionTime = self.RECORD_SCHEMA.field_map["decommissionTime"].default
        self.note = str()
        self.actor = str()
    
    
    @property
    def deprecated(self) -> bool:
        """Getter: Whether the entity is deprecated."""
        return self._inner_dict.get('deprecated')  # type: ignore
    
    
    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        """Setter: Whether the entity is deprecated."""
        self._inner_dict['deprecated'] = value
    
    
    @property
    def decommissionTime(self) -> Union[None, int]:
        """Getter: The time user plan to decommission this entity."""
        return self._inner_dict.get('decommissionTime')  # type: ignore
    
    
    @decommissionTime.setter
    def decommissionTime(self, value: Union[None, int]) -> None:
        """Setter: The time user plan to decommission this entity."""
        self._inner_dict['decommissionTime'] = value
    
    
    @property
    def note(self) -> str:
        """Getter: Additional information about the entity deprecation plan, such as the wiki, doc, RB."""
        return self._inner_dict.get('note')  # type: ignore
    
    
    @note.setter
    def note(self, value: str) -> None:
        """Setter: Additional information about the entity deprecation plan, such as the wiki, doc, RB."""
        self._inner_dict['note'] = value
    
    
    @property
    def actor(self) -> str:
        """Getter: The corpuser URN which will be credited for modifying this deprecation content."""
        return self._inner_dict.get('actor')  # type: ignore
    
    
    @actor.setter
    def actor(self, value: str) -> None:
        """Setter: The corpuser URN which will be credited for modifying this deprecation content."""
        self._inner_dict['actor'] = value
    
    
class GlobalTagsClass(DictWrapper):
    """Tag aspect used for applying tags to an entity"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.GlobalTags")
    def __init__(self,
        tags: List["TagAssociationClass"],
    ):
        super().__init__()
        
        self.tags = tags
    
    @classmethod
    def construct_with_defaults(cls) -> "GlobalTagsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.tags = list()
    
    
    @property
    def tags(self) -> List["TagAssociationClass"]:
        """Getter: Tags associated with a given entity"""
        return self._inner_dict.get('tags')  # type: ignore
    
    
    @tags.setter
    def tags(self, value: List["TagAssociationClass"]) -> None:
        """Setter: Tags associated with a given entity"""
        self._inner_dict['tags'] = value
    
    
class GlossaryTermAssociationClass(DictWrapper):
    """Properties of an applied glossary term."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.GlossaryTermAssociation")
    def __init__(self,
        urn: str,
    ):
        super().__init__()
        
        self.urn = urn
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryTermAssociationClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
    
    
    @property
    def urn(self) -> str:
        """Getter: Urn of the applied glossary term"""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: Urn of the applied glossary term"""
        self._inner_dict['urn'] = value
    
    
class GlossaryTermsClass(DictWrapper):
    """Related business terms information"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.GlossaryTerms")
    def __init__(self,
        terms: List["GlossaryTermAssociationClass"],
        auditStamp: "AuditStampClass",
    ):
        super().__init__()
        
        self.terms = terms
        self.auditStamp = auditStamp
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryTermsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.terms = list()
        self.auditStamp = AuditStampClass.construct_with_defaults()
    
    
    @property
    def terms(self) -> List["GlossaryTermAssociationClass"]:
        """Getter: The related business terms"""
        return self._inner_dict.get('terms')  # type: ignore
    
    
    @terms.setter
    def terms(self, value: List["GlossaryTermAssociationClass"]) -> None:
        """Setter: The related business terms"""
        self._inner_dict['terms'] = value
    
    
    @property
    def auditStamp(self) -> "AuditStampClass":
        """Getter: Audit stamp containing who reported the related business term"""
        return self._inner_dict.get('auditStamp')  # type: ignore
    
    
    @auditStamp.setter
    def auditStamp(self, value: "AuditStampClass") -> None:
        """Setter: Audit stamp containing who reported the related business term"""
        self._inner_dict['auditStamp'] = value
    
    
class InstitutionalMemoryClass(DictWrapper):
    """Institutional memory of an entity. This is a way to link to relevant documentation and provide description of the documentation. Institutional or tribal knowledge is very important for users to leverage the entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.InstitutionalMemory")
    def __init__(self,
        elements: List["InstitutionalMemoryMetadataClass"],
    ):
        super().__init__()
        
        self.elements = elements
    
    @classmethod
    def construct_with_defaults(cls) -> "InstitutionalMemoryClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.elements = list()
    
    
    @property
    def elements(self) -> List["InstitutionalMemoryMetadataClass"]:
        """Getter: List of records that represent institutional memory of an entity. Each record consists of a link, description, creator and timestamps associated with that record."""
        return self._inner_dict.get('elements')  # type: ignore
    
    
    @elements.setter
    def elements(self, value: List["InstitutionalMemoryMetadataClass"]) -> None:
        """Setter: List of records that represent institutional memory of an entity. Each record consists of a link, description, creator and timestamps associated with that record."""
        self._inner_dict['elements'] = value
    
    
class InstitutionalMemoryMetadataClass(DictWrapper):
    """Metadata corresponding to a record of institutional memory."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.InstitutionalMemoryMetadata")
    def __init__(self,
        url: str,
        description: str,
        createStamp: "AuditStampClass",
    ):
        super().__init__()
        
        self.url = url
        self.description = description
        self.createStamp = createStamp
    
    @classmethod
    def construct_with_defaults(cls) -> "InstitutionalMemoryMetadataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.url = str()
        self.description = str()
        self.createStamp = AuditStampClass.construct_with_defaults()
    
    
    @property
    def url(self) -> str:
        """Getter: Link to an engineering design document or a wiki page."""
        return self._inner_dict.get('url')  # type: ignore
    
    
    @url.setter
    def url(self, value: str) -> None:
        """Setter: Link to an engineering design document or a wiki page."""
        self._inner_dict['url'] = value
    
    
    @property
    def description(self) -> str:
        """Getter: Description of the link."""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: str) -> None:
        """Setter: Description of the link."""
        self._inner_dict['description'] = value
    
    
    @property
    def createStamp(self) -> "AuditStampClass":
        """Getter: Audit stamp associated with creation of this record"""
        return self._inner_dict.get('createStamp')  # type: ignore
    
    
    @createStamp.setter
    def createStamp(self, value: "AuditStampClass") -> None:
        """Setter: Audit stamp associated with creation of this record"""
        self._inner_dict['createStamp'] = value
    
    
class MLFeatureDataTypeClass(object):
    """MLFeature Data Type"""
    
    
    """Useless data is unique, discrete data with no potential relationship with the outcome variable.
    A useless feature has high cardinality. An example would be bank account numbers that were generated randomly."""
    USELESS = "USELESS"
    
    """Nominal data is made of discrete values with no numerical relationship between the different categories — mean and median are meaningless.
    Animal species is one example. For example, pig is not higher than bird and lower than fish."""
    NOMINAL = "NOMINAL"
    
    """Ordinal data are discrete integers that can be ranked or sorted.
    For example, the distance between first and second may not be the same as the distance between second and third."""
    ORDINAL = "ORDINAL"
    
    """Binary data is discrete data that can be in only one of two categories — either yes or no, 1 or 0, off or on, etc"""
    BINARY = "BINARY"
    
    """Count data is discrete whole number data — no negative numbers here.
    Count data often has many small values, such as zero and one."""
    COUNT = "COUNT"
    
    """Time data is a cyclical, repeating continuous form of data.
    The relevant time features can be any period— daily, weekly, monthly, annual, etc."""
    TIME = "TIME"
    
    """Interval data has equal spaces between the numbers and does not represent a temporal pattern.
    Examples include percentages, temperatures, and income."""
    INTERVAL = "INTERVAL"
    
    """Image Data"""
    IMAGE = "IMAGE"
    
    """Video Data"""
    VIDEO = "VIDEO"
    
    """Audio Data"""
    AUDIO = "AUDIO"
    
    """Text Data"""
    TEXT = "TEXT"
    
    """Mapping Data Type ex: dict, map"""
    MAP = "MAP"
    
    """Sequence Data Type ex: list, tuple, range"""
    SEQUENCE = "SEQUENCE"
    
    """Set Data Type ex: set, frozenset"""
    SET = "SET"
    
    
class OwnerClass(DictWrapper):
    """Ownership information"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.Owner")
    def __init__(self,
        owner: str,
        type: Union[str, "OwnershipTypeClass"],
        source: Union[None, "OwnershipSourceClass"]=None,
    ):
        super().__init__()
        
        self.owner = owner
        self.type = type
        self.source = source
    
    @classmethod
    def construct_with_defaults(cls) -> "OwnerClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.owner = str()
        self.type = OwnershipTypeClass.DEVELOPER
        self.source = self.RECORD_SCHEMA.field_map["source"].default
    
    
    @property
    def owner(self) -> str:
        """Getter: Owner URN, e.g. urn:li:corpuser:ldap, urn:li:corpGroup:group_name, and urn:li:multiProduct:mp_name
    (Caveat: only corpuser is currently supported in the frontend.)"""
        return self._inner_dict.get('owner')  # type: ignore
    
    
    @owner.setter
    def owner(self, value: str) -> None:
        """Setter: Owner URN, e.g. urn:li:corpuser:ldap, urn:li:corpGroup:group_name, and urn:li:multiProduct:mp_name
    (Caveat: only corpuser is currently supported in the frontend.)"""
        self._inner_dict['owner'] = value
    
    
    @property
    def type(self) -> Union[str, "OwnershipTypeClass"]:
        """Getter: The type of the ownership"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "OwnershipTypeClass"]) -> None:
        """Setter: The type of the ownership"""
        self._inner_dict['type'] = value
    
    
    @property
    def source(self) -> Union[None, "OwnershipSourceClass"]:
        """Getter: Source information for the ownership"""
        return self._inner_dict.get('source')  # type: ignore
    
    
    @source.setter
    def source(self, value: Union[None, "OwnershipSourceClass"]) -> None:
        """Setter: Source information for the ownership"""
        self._inner_dict['source'] = value
    
    
class OwnershipClass(DictWrapper):
    """Ownership information of an entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.Ownership")
    def __init__(self,
        owners: List["OwnerClass"],
        lastModified: "AuditStampClass",
    ):
        super().__init__()
        
        self.owners = owners
        self.lastModified = lastModified
    
    @classmethod
    def construct_with_defaults(cls) -> "OwnershipClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.owners = list()
        self.lastModified = AuditStampClass.construct_with_defaults()
    
    
    @property
    def owners(self) -> List["OwnerClass"]:
        """Getter: List of owners of the entity."""
        return self._inner_dict.get('owners')  # type: ignore
    
    
    @owners.setter
    def owners(self, value: List["OwnerClass"]) -> None:
        """Setter: List of owners of the entity."""
        self._inner_dict['owners'] = value
    
    
    @property
    def lastModified(self) -> "AuditStampClass":
        """Getter: Audit stamp containing who last modified the record and when."""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "AuditStampClass") -> None:
        """Setter: Audit stamp containing who last modified the record and when."""
        self._inner_dict['lastModified'] = value
    
    
class OwnershipSourceClass(DictWrapper):
    """Source/provider of the ownership information"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.OwnershipSource")
    def __init__(self,
        type: Union[str, "OwnershipSourceTypeClass"],
        url: Union[None, str]=None,
    ):
        super().__init__()
        
        self.type = type
        self.url = url
    
    @classmethod
    def construct_with_defaults(cls) -> "OwnershipSourceClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.type = OwnershipSourceTypeClass.AUDIT
        self.url = self.RECORD_SCHEMA.field_map["url"].default
    
    
    @property
    def type(self) -> Union[str, "OwnershipSourceTypeClass"]:
        """Getter: The type of the source"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "OwnershipSourceTypeClass"]) -> None:
        """Setter: The type of the source"""
        self._inner_dict['type'] = value
    
    
    @property
    def url(self) -> Union[None, str]:
        """Getter: A reference URL for the source"""
        return self._inner_dict.get('url')  # type: ignore
    
    
    @url.setter
    def url(self, value: Union[None, str]) -> None:
        """Setter: A reference URL for the source"""
        self._inner_dict['url'] = value
    
    
class OwnershipSourceTypeClass(object):
    # No docs available.
    
    
    """Auditing system or audit logs"""
    AUDIT = "AUDIT"
    
    """Database, e.g. GRANTS table"""
    DATABASE = "DATABASE"
    
    """File system, e.g. file/directory owner"""
    FILE_SYSTEM = "FILE_SYSTEM"
    
    """Issue tracking system, e.g. Jira"""
    ISSUE_TRACKING_SYSTEM = "ISSUE_TRACKING_SYSTEM"
    
    """Manually provided by a user"""
    MANUAL = "MANUAL"
    
    """Other ownership-like service, e.g. Nuage, ACL service etc"""
    SERVICE = "SERVICE"
    
    """SCM system, e.g. GIT, SVN"""
    SOURCE_CONTROL = "SOURCE_CONTROL"
    
    """Other sources"""
    OTHER = "OTHER"
    
    
class OwnershipTypeClass(object):
    """Owner category or owner role"""
    
    
    """A person or group that is in charge of developing the code"""
    DEVELOPER = "DEVELOPER"
    
    """A person or group that is owning the data"""
    DATAOWNER = "DATAOWNER"
    
    """A person or a group that overseas the operation, e.g. a DBA or SRE."""
    DELEGATE = "DELEGATE"
    
    """A person, group, or service that produces/generates the data"""
    PRODUCER = "PRODUCER"
    
    """A person, group, or service that consumes the data"""
    CONSUMER = "CONSUMER"
    
    """A person or a group that has direct business interest"""
    STAKEHOLDER = "STAKEHOLDER"
    
    
class StatusClass(DictWrapper):
    """The status metadata of an entity, e.g. dataset, metric, feature, etc."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.Status")
    def __init__(self,
        removed: Optional[bool]=None,
    ):
        super().__init__()
        
        if removed is None:
            self.removed = False
        else:
            self.removed = removed
    
    @classmethod
    def construct_with_defaults(cls) -> "StatusClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.removed = self.RECORD_SCHEMA.field_map["removed"].default
    
    
    @property
    def removed(self) -> bool:
        """Getter: whether the entity is removed or not"""
        return self._inner_dict.get('removed')  # type: ignore
    
    
    @removed.setter
    def removed(self, value: bool) -> None:
        """Setter: whether the entity is removed or not"""
        self._inner_dict['removed'] = value
    
    
class TagAssociationClass(DictWrapper):
    """Properties of an applied tag. For now, just an Urn. In the future we can extend this with other properties, e.g.
    propagation parameters."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.TagAssociation")
    def __init__(self,
        tag: str,
    ):
        super().__init__()
        
        self.tag = tag
    
    @classmethod
    def construct_with_defaults(cls) -> "TagAssociationClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.tag = str()
    
    
    @property
    def tag(self) -> str:
        """Getter: Urn of the applied tag"""
        return self._inner_dict.get('tag')  # type: ignore
    
    
    @tag.setter
    def tag(self, value: str) -> None:
        """Setter: Urn of the applied tag"""
        self._inner_dict['tag'] = value
    
    
class VersionTagClass(DictWrapper):
    """A resource-defined string representing the resource state for the purpose of concurrency control"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.VersionTag")
    def __init__(self,
        versionTag: Union[None, str]=None,
    ):
        super().__init__()
        
        self.versionTag = versionTag
    
    @classmethod
    def construct_with_defaults(cls) -> "VersionTagClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.versionTag = self.RECORD_SCHEMA.field_map["versionTag"].default
    
    
    @property
    def versionTag(self) -> Union[None, str]:
        # No docs available.
        return self._inner_dict.get('versionTag')  # type: ignore
    
    
    @versionTag.setter
    def versionTag(self, value: Union[None, str]) -> None:
        # No docs available.
        self._inner_dict['versionTag'] = value
    
    
class TransformationTypeClass(object):
    """Type of the transformation involved in generating destination fields from source fields."""
    
    
    """Field transformation expressed as unknown black box function."""
    BLACKBOX = "BLACKBOX"
    
    """Field transformation expressed as Identity function."""
    IDENTITY = "IDENTITY"
    
    
class UDFTransformerClass(DictWrapper):
    """Field transformation expressed in UDF"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.common.fieldtransformer.UDFTransformer")
    def __init__(self,
        udf: str,
    ):
        super().__init__()
        
        self.udf = udf
    
    @classmethod
    def construct_with_defaults(cls) -> "UDFTransformerClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.udf = str()
    
    
    @property
    def udf(self) -> str:
        """Getter: A UDF mentioning how the source fields got transformed to destination field. This is the FQCN(Fully Qualified Class Name) of the udf."""
        return self._inner_dict.get('udf')  # type: ignore
    
    
    @udf.setter
    def udf(self, value: str) -> None:
        """Setter: A UDF mentioning how the source fields got transformed to destination field. This is the FQCN(Fully Qualified Class Name) of the udf."""
        self._inner_dict['udf'] = value
    
    
class DashboardInfoClass(DictWrapper):
    """Information about a dashboard"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dashboard.DashboardInfo")
    def __init__(self,
        title: str,
        description: str,
        lastModified: "ChangeAuditStampsClass",
        customProperties: Optional[Dict[str, str]]=None,
        externalUrl: Union[None, str]=None,
        charts: Optional[List[str]]=None,
        dashboardUrl: Union[None, str]=None,
        access: Union[None, Union[str, "AccessLevelClass"]]=None,
        lastRefreshed: Union[None, int]=None,
    ):
        super().__init__()
        
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
        self.externalUrl = externalUrl
        self.title = title
        self.description = description
        if charts is None:
            self.charts = []
        else:
            self.charts = charts
        self.lastModified = lastModified
        self.dashboardUrl = dashboardUrl
        self.access = access
        self.lastRefreshed = lastRefreshed
    
    @classmethod
    def construct_with_defaults(cls) -> "DashboardInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.customProperties = dict()
        self.externalUrl = self.RECORD_SCHEMA.field_map["externalUrl"].default
        self.title = str()
        self.description = str()
        self.charts = list()
        self.lastModified = ChangeAuditStampsClass.construct_with_defaults()
        self.dashboardUrl = self.RECORD_SCHEMA.field_map["dashboardUrl"].default
        self.access = self.RECORD_SCHEMA.field_map["access"].default
        self.lastRefreshed = self.RECORD_SCHEMA.field_map["lastRefreshed"].default
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: Custom property bag."""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: Custom property bag."""
        self._inner_dict['customProperties'] = value
    
    
    @property
    def externalUrl(self) -> Union[None, str]:
        """Getter: URL where the reference exist"""
        return self._inner_dict.get('externalUrl')  # type: ignore
    
    
    @externalUrl.setter
    def externalUrl(self, value: Union[None, str]) -> None:
        """Setter: URL where the reference exist"""
        self._inner_dict['externalUrl'] = value
    
    
    @property
    def title(self) -> str:
        """Getter: Title of the dashboard"""
        return self._inner_dict.get('title')  # type: ignore
    
    
    @title.setter
    def title(self, value: str) -> None:
        """Setter: Title of the dashboard"""
        self._inner_dict['title'] = value
    
    
    @property
    def description(self) -> str:
        """Getter: Detailed description about the dashboard"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: str) -> None:
        """Setter: Detailed description about the dashboard"""
        self._inner_dict['description'] = value
    
    
    @property
    def charts(self) -> List[str]:
        """Getter: Charts in a dashboard"""
        return self._inner_dict.get('charts')  # type: ignore
    
    
    @charts.setter
    def charts(self, value: List[str]) -> None:
        """Setter: Charts in a dashboard"""
        self._inner_dict['charts'] = value
    
    
    @property
    def lastModified(self) -> "ChangeAuditStampsClass":
        """Getter: Captures information about who created/last modified/deleted this dashboard and when"""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "ChangeAuditStampsClass") -> None:
        """Setter: Captures information about who created/last modified/deleted this dashboard and when"""
        self._inner_dict['lastModified'] = value
    
    
    @property
    def dashboardUrl(self) -> Union[None, str]:
        """Getter: URL for the dashboard. This could be used as an external link on DataHub to allow users access/view the dashboard"""
        return self._inner_dict.get('dashboardUrl')  # type: ignore
    
    
    @dashboardUrl.setter
    def dashboardUrl(self, value: Union[None, str]) -> None:
        """Setter: URL for the dashboard. This could be used as an external link on DataHub to allow users access/view the dashboard"""
        self._inner_dict['dashboardUrl'] = value
    
    
    @property
    def access(self) -> Union[None, Union[str, "AccessLevelClass"]]:
        """Getter: Access level for the dashboard"""
        return self._inner_dict.get('access')  # type: ignore
    
    
    @access.setter
    def access(self, value: Union[None, Union[str, "AccessLevelClass"]]) -> None:
        """Setter: Access level for the dashboard"""
        self._inner_dict['access'] = value
    
    
    @property
    def lastRefreshed(self) -> Union[None, int]:
        """Getter: The time when this dashboard last refreshed"""
        return self._inner_dict.get('lastRefreshed')  # type: ignore
    
    
    @lastRefreshed.setter
    def lastRefreshed(self, value: Union[None, int]) -> None:
        """Setter: The time when this dashboard last refreshed"""
        self._inner_dict['lastRefreshed'] = value
    
    
class DataFlowInfoClass(DictWrapper):
    """Information about a Data processing flow"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.datajob.DataFlowInfo")
    def __init__(self,
        name: str,
        customProperties: Optional[Dict[str, str]]=None,
        externalUrl: Union[None, str]=None,
        description: Union[None, str]=None,
        project: Union[None, str]=None,
    ):
        super().__init__()
        
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
        self.externalUrl = externalUrl
        self.name = name
        self.description = description
        self.project = project
    
    @classmethod
    def construct_with_defaults(cls) -> "DataFlowInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.customProperties = dict()
        self.externalUrl = self.RECORD_SCHEMA.field_map["externalUrl"].default
        self.name = str()
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.project = self.RECORD_SCHEMA.field_map["project"].default
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: Custom property bag."""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: Custom property bag."""
        self._inner_dict['customProperties'] = value
    
    
    @property
    def externalUrl(self) -> Union[None, str]:
        """Getter: URL where the reference exist"""
        return self._inner_dict.get('externalUrl')  # type: ignore
    
    
    @externalUrl.setter
    def externalUrl(self, value: Union[None, str]) -> None:
        """Setter: URL where the reference exist"""
        self._inner_dict['externalUrl'] = value
    
    
    @property
    def name(self) -> str:
        """Getter: Flow name"""
        return self._inner_dict.get('name')  # type: ignore
    
    
    @name.setter
    def name(self, value: str) -> None:
        """Setter: Flow name"""
        self._inner_dict['name'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Flow description"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Flow description"""
        self._inner_dict['description'] = value
    
    
    @property
    def project(self) -> Union[None, str]:
        """Getter: Optional project/namespace associated with the flow"""
        return self._inner_dict.get('project')  # type: ignore
    
    
    @project.setter
    def project(self, value: Union[None, str]) -> None:
        """Setter: Optional project/namespace associated with the flow"""
        self._inner_dict['project'] = value
    
    
class DataJobInfoClass(DictWrapper):
    """Information about a Data processing job"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.datajob.DataJobInfo")
    def __init__(self,
        name: str,
        type: Union[str, "AzkabanJobTypeClass"],
        customProperties: Optional[Dict[str, str]]=None,
        externalUrl: Union[None, str]=None,
        description: Union[None, str]=None,
        flowUrn: Union[None, str]=None,
    ):
        super().__init__()
        
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
        self.externalUrl = externalUrl
        self.name = name
        self.description = description
        self.type = type
        self.flowUrn = flowUrn
    
    @classmethod
    def construct_with_defaults(cls) -> "DataJobInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.customProperties = dict()
        self.externalUrl = self.RECORD_SCHEMA.field_map["externalUrl"].default
        self.name = str()
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.type = AzkabanJobTypeClass.COMMAND
        self.flowUrn = self.RECORD_SCHEMA.field_map["flowUrn"].default
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: Custom property bag."""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: Custom property bag."""
        self._inner_dict['customProperties'] = value
    
    
    @property
    def externalUrl(self) -> Union[None, str]:
        """Getter: URL where the reference exist"""
        return self._inner_dict.get('externalUrl')  # type: ignore
    
    
    @externalUrl.setter
    def externalUrl(self, value: Union[None, str]) -> None:
        """Setter: URL where the reference exist"""
        self._inner_dict['externalUrl'] = value
    
    
    @property
    def name(self) -> str:
        """Getter: Job name"""
        return self._inner_dict.get('name')  # type: ignore
    
    
    @name.setter
    def name(self, value: str) -> None:
        """Setter: Job name"""
        self._inner_dict['name'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Job description"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Job description"""
        self._inner_dict['description'] = value
    
    
    @property
    def type(self) -> Union[str, "AzkabanJobTypeClass"]:
        """Getter: Datajob type"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "AzkabanJobTypeClass"]) -> None:
        """Setter: Datajob type"""
        self._inner_dict['type'] = value
    
    
    @property
    def flowUrn(self) -> Union[None, str]:
        """Getter: DataFlow urn that this job is part of"""
        return self._inner_dict.get('flowUrn')  # type: ignore
    
    
    @flowUrn.setter
    def flowUrn(self, value: Union[None, str]) -> None:
        """Setter: DataFlow urn that this job is part of"""
        self._inner_dict['flowUrn'] = value
    
    
class DataJobInputOutputClass(DictWrapper):
    """Information about the inputs and outputs of a Data processing job"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.datajob.DataJobInputOutput")
    def __init__(self,
        inputDatasets: List[str],
        outputDatasets: List[str],
        inputDatajobs: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.inputDatasets = inputDatasets
        self.outputDatasets = outputDatasets
        self.inputDatajobs = inputDatajobs
    
    @classmethod
    def construct_with_defaults(cls) -> "DataJobInputOutputClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.inputDatasets = list()
        self.outputDatasets = list()
        self.inputDatajobs = self.RECORD_SCHEMA.field_map["inputDatajobs"].default
    
    
    @property
    def inputDatasets(self) -> List[str]:
        """Getter: Input datasets consumed by the data job during processing"""
        return self._inner_dict.get('inputDatasets')  # type: ignore
    
    
    @inputDatasets.setter
    def inputDatasets(self, value: List[str]) -> None:
        """Setter: Input datasets consumed by the data job during processing"""
        self._inner_dict['inputDatasets'] = value
    
    
    @property
    def outputDatasets(self) -> List[str]:
        """Getter: Output datasets produced by the data job during processing"""
        return self._inner_dict.get('outputDatasets')  # type: ignore
    
    
    @outputDatasets.setter
    def outputDatasets(self, value: List[str]) -> None:
        """Setter: Output datasets produced by the data job during processing"""
        self._inner_dict['outputDatasets'] = value
    
    
    @property
    def inputDatajobs(self) -> Union[None, List[str]]:
        """Getter: Input datajobs that this data job depends on"""
        return self._inner_dict.get('inputDatajobs')  # type: ignore
    
    
    @inputDatajobs.setter
    def inputDatajobs(self, value: Union[None, List[str]]) -> None:
        """Setter: Input datajobs that this data job depends on"""
        self._inner_dict['inputDatajobs'] = value
    
    
class AzkabanJobTypeClass(object):
    """The various types of support azkaban jobs"""
    
    
    """The command job type is one of the basic built-in types. It runs multiple UNIX commands using java processbuilder.
    Upon execution, Azkaban spawns off a process to run the command."""
    COMMAND = "COMMAND"
    
    """Runs a java program with ability to access Hadoop cluster.
    https://azkaban.readthedocs.io/en/latest/jobTypes.html#java-job-type"""
    HADOOP_JAVA = "HADOOP_JAVA"
    
    """In large part, this is the same Command type. The difference is its ability to talk to a Hadoop cluster
    securely, via Hadoop tokens."""
    HADOOP_SHELL = "HADOOP_SHELL"
    
    """Hive type is for running Hive jobs."""
    HIVE = "HIVE"
    
    """Pig type is for running Pig jobs."""
    PIG = "PIG"
    
    """SQL is for running Presto, mysql queries etc"""
    SQL = "SQL"
    
    
class DataProcessInfoClass(DictWrapper):
    """The inputs and outputs of this data process"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataprocess.DataProcessInfo")
    def __init__(self,
        inputs: Union[None, List[str]]=None,
        outputs: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.inputs = inputs
        self.outputs = outputs
    
    @classmethod
    def construct_with_defaults(cls) -> "DataProcessInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.inputs = self.RECORD_SCHEMA.field_map["inputs"].default
        self.outputs = self.RECORD_SCHEMA.field_map["outputs"].default
    
    
    @property
    def inputs(self) -> Union[None, List[str]]:
        """Getter: the inputs of the data process"""
        return self._inner_dict.get('inputs')  # type: ignore
    
    
    @inputs.setter
    def inputs(self, value: Union[None, List[str]]) -> None:
        """Setter: the inputs of the data process"""
        self._inner_dict['inputs'] = value
    
    
    @property
    def outputs(self) -> Union[None, List[str]]:
        """Getter: the outputs of the data process"""
        return self._inner_dict.get('outputs')  # type: ignore
    
    
    @outputs.setter
    def outputs(self, value: Union[None, List[str]]) -> None:
        """Setter: the outputs of the data process"""
        self._inner_dict['outputs'] = value
    
    
class DatasetDeprecationClass(DictWrapper):
    """Dataset deprecation status"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.DatasetDeprecation")
    def __init__(self,
        deprecated: bool,
        note: str,
        decommissionTime: Union[None, int]=None,
        actor: Union[None, str]=None,
    ):
        super().__init__()
        
        self.deprecated = deprecated
        self.decommissionTime = decommissionTime
        self.note = note
        self.actor = actor
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetDeprecationClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.deprecated = bool()
        self.decommissionTime = self.RECORD_SCHEMA.field_map["decommissionTime"].default
        self.note = str()
        self.actor = self.RECORD_SCHEMA.field_map["actor"].default
    
    
    @property
    def deprecated(self) -> bool:
        """Getter: Whether the dataset is deprecated by owner."""
        return self._inner_dict.get('deprecated')  # type: ignore
    
    
    @deprecated.setter
    def deprecated(self, value: bool) -> None:
        """Setter: Whether the dataset is deprecated by owner."""
        self._inner_dict['deprecated'] = value
    
    
    @property
    def decommissionTime(self) -> Union[None, int]:
        """Getter: The time user plan to decommission this dataset."""
        return self._inner_dict.get('decommissionTime')  # type: ignore
    
    
    @decommissionTime.setter
    def decommissionTime(self, value: Union[None, int]) -> None:
        """Setter: The time user plan to decommission this dataset."""
        self._inner_dict['decommissionTime'] = value
    
    
    @property
    def note(self) -> str:
        """Getter: Additional information about the dataset deprecation plan, such as the wiki, doc, RB."""
        return self._inner_dict.get('note')  # type: ignore
    
    
    @note.setter
    def note(self, value: str) -> None:
        """Setter: Additional information about the dataset deprecation plan, such as the wiki, doc, RB."""
        self._inner_dict['note'] = value
    
    
    @property
    def actor(self) -> Union[None, str]:
        """Getter: The corpuser URN which will be credited for modifying this deprecation content."""
        return self._inner_dict.get('actor')  # type: ignore
    
    
    @actor.setter
    def actor(self, value: Union[None, str]) -> None:
        """Setter: The corpuser URN which will be credited for modifying this deprecation content."""
        self._inner_dict['actor'] = value
    
    
class DatasetFieldMappingClass(DictWrapper):
    """Representation of mapping between fields in source dataset to the field in destination dataset"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.DatasetFieldMapping")
    def __init__(self,
        created: "AuditStampClass",
        transformation: Union[Union[str, "TransformationTypeClass"], "UDFTransformerClass"],
        sourceFields: List[str],
        destinationField: str,
    ):
        super().__init__()
        
        self.created = created
        self.transformation = transformation
        self.sourceFields = sourceFields
        self.destinationField = destinationField
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetFieldMappingClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.created = AuditStampClass.construct_with_defaults()
        self.transformation = TransformationTypeClass.BLACKBOX
        self.sourceFields = list()
        self.destinationField = str()
    
    
    @property
    def created(self) -> "AuditStampClass":
        """Getter: Audit stamp containing who reported the field mapping and when"""
        return self._inner_dict.get('created')  # type: ignore
    
    
    @created.setter
    def created(self, value: "AuditStampClass") -> None:
        """Setter: Audit stamp containing who reported the field mapping and when"""
        self._inner_dict['created'] = value
    
    
    @property
    def transformation(self) -> Union[Union[str, "TransformationTypeClass"], "UDFTransformerClass"]:
        """Getter: Transfomration function between the fields involved"""
        return self._inner_dict.get('transformation')  # type: ignore
    
    
    @transformation.setter
    def transformation(self, value: Union[Union[str, "TransformationTypeClass"], "UDFTransformerClass"]) -> None:
        """Setter: Transfomration function between the fields involved"""
        self._inner_dict['transformation'] = value
    
    
    @property
    def sourceFields(self) -> List[str]:
        """Getter: Source fields from which the fine grained lineage is derived"""
        return self._inner_dict.get('sourceFields')  # type: ignore
    
    
    @sourceFields.setter
    def sourceFields(self, value: List[str]) -> None:
        """Setter: Source fields from which the fine grained lineage is derived"""
        self._inner_dict['sourceFields'] = value
    
    
    @property
    def destinationField(self) -> str:
        """Getter: Destination field which is derived from source fields"""
        return self._inner_dict.get('destinationField')  # type: ignore
    
    
    @destinationField.setter
    def destinationField(self, value: str) -> None:
        """Setter: Destination field which is derived from source fields"""
        self._inner_dict['destinationField'] = value
    
    
class DatasetLineageTypeClass(object):
    """The various types of supported dataset lineage"""
    
    
    """Direct copy without modification"""
    COPY = "COPY"
    
    """Transformed data with modification (format or content change)"""
    TRANSFORMED = "TRANSFORMED"
    
    """Represents a view defined on the sources e.g. Hive view defined on underlying hive tables or a Hive table pointing to a HDFS dataset or DALI view defined on multiple sources"""
    VIEW = "VIEW"
    
    
class DatasetPropertiesClass(DictWrapper):
    """Properties associated with a Dataset"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.DatasetProperties")
    def __init__(self,
        customProperties: Optional[Dict[str, str]]=None,
        externalUrl: Union[None, str]=None,
        description: Union[None, str]=None,
        uri: Union[None, str]=None,
        tags: Optional[List[str]]=None,
    ):
        super().__init__()
        
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
        self.externalUrl = externalUrl
        self.description = description
        self.uri = uri
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetPropertiesClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.customProperties = dict()
        self.externalUrl = self.RECORD_SCHEMA.field_map["externalUrl"].default
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.uri = self.RECORD_SCHEMA.field_map["uri"].default
        self.tags = list()
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: Custom property bag."""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: Custom property bag."""
        self._inner_dict['customProperties'] = value
    
    
    @property
    def externalUrl(self) -> Union[None, str]:
        """Getter: URL where the reference exist"""
        return self._inner_dict.get('externalUrl')  # type: ignore
    
    
    @externalUrl.setter
    def externalUrl(self, value: Union[None, str]) -> None:
        """Setter: URL where the reference exist"""
        self._inner_dict['externalUrl'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Documentation of the dataset"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Documentation of the dataset"""
        self._inner_dict['description'] = value
    
    
    @property
    def uri(self) -> Union[None, str]:
        """Getter: The abstracted URI such as hdfs:///data/tracking/PageViewEvent, file:///dir/file_name. Uri should not include any environment specific properties. Some datasets might not have a standardized uri, which makes this field optional (i.e. kafka topic)."""
        return self._inner_dict.get('uri')  # type: ignore
    
    
    @uri.setter
    def uri(self, value: Union[None, str]) -> None:
        """Setter: The abstracted URI such as hdfs:///data/tracking/PageViewEvent, file:///dir/file_name. Uri should not include any environment specific properties. Some datasets might not have a standardized uri, which makes this field optional (i.e. kafka topic)."""
        self._inner_dict['uri'] = value
    
    
    @property
    def tags(self) -> List[str]:
        """Getter: [Legacy] Unstructured tags for the dataset. Structured tags can be applied via the `GlobalTags` aspect."""
        return self._inner_dict.get('tags')  # type: ignore
    
    
    @tags.setter
    def tags(self, value: List[str]) -> None:
        """Setter: [Legacy] Unstructured tags for the dataset. Structured tags can be applied via the `GlobalTags` aspect."""
        self._inner_dict['tags'] = value
    
    
class DatasetUpstreamLineageClass(DictWrapper):
    """Fine Grained upstream lineage for fields in a dataset"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.DatasetUpstreamLineage")
    def __init__(self,
        fieldMappings: List["DatasetFieldMappingClass"],
    ):
        super().__init__()
        
        self.fieldMappings = fieldMappings
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetUpstreamLineageClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.fieldMappings = list()
    
    
    @property
    def fieldMappings(self) -> List["DatasetFieldMappingClass"]:
        """Getter: Upstream to downstream field level lineage mappings"""
        return self._inner_dict.get('fieldMappings')  # type: ignore
    
    
    @fieldMappings.setter
    def fieldMappings(self, value: List["DatasetFieldMappingClass"]) -> None:
        """Setter: Upstream to downstream field level lineage mappings"""
        self._inner_dict['fieldMappings'] = value
    
    
class UpstreamClass(DictWrapper):
    """Upstream lineage information about a dataset including the source reporting the lineage"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.Upstream")
    def __init__(self,
        auditStamp: "AuditStampClass",
        dataset: str,
        type: Union[str, "DatasetLineageTypeClass"],
    ):
        super().__init__()
        
        self.auditStamp = auditStamp
        self.dataset = dataset
        self.type = type
    
    @classmethod
    def construct_with_defaults(cls) -> "UpstreamClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.auditStamp = AuditStampClass.construct_with_defaults()
        self.dataset = str()
        self.type = DatasetLineageTypeClass.COPY
    
    
    @property
    def auditStamp(self) -> "AuditStampClass":
        """Getter: Audit stamp containing who reported the lineage and when"""
        return self._inner_dict.get('auditStamp')  # type: ignore
    
    
    @auditStamp.setter
    def auditStamp(self, value: "AuditStampClass") -> None:
        """Setter: Audit stamp containing who reported the lineage and when"""
        self._inner_dict['auditStamp'] = value
    
    
    @property
    def dataset(self) -> str:
        """Getter: The upstream dataset the lineage points to"""
        return self._inner_dict.get('dataset')  # type: ignore
    
    
    @dataset.setter
    def dataset(self, value: str) -> None:
        """Setter: The upstream dataset the lineage points to"""
        self._inner_dict['dataset'] = value
    
    
    @property
    def type(self) -> Union[str, "DatasetLineageTypeClass"]:
        """Getter: The type of the lineage"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "DatasetLineageTypeClass"]) -> None:
        """Setter: The type of the lineage"""
        self._inner_dict['type'] = value
    
    
class UpstreamLineageClass(DictWrapper):
    """Upstream lineage of a dataset"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.dataset.UpstreamLineage")
    def __init__(self,
        upstreams: List["UpstreamClass"],
    ):
        super().__init__()
        
        self.upstreams = upstreams
    
    @classmethod
    def construct_with_defaults(cls) -> "UpstreamLineageClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.upstreams = list()
    
    
    @property
    def upstreams(self) -> List["UpstreamClass"]:
        """Getter: List of upstream dataset lineage information"""
        return self._inner_dict.get('upstreams')  # type: ignore
    
    
    @upstreams.setter
    def upstreams(self, value: List["UpstreamClass"]) -> None:
        """Setter: List of upstream dataset lineage information"""
        self._inner_dict['upstreams'] = value
    
    
class GlossaryNodeInfoClass(DictWrapper):
    """Properties associated with a GlossaryNode"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.glossary.GlossaryNodeInfo")
    def __init__(self,
        definition: str,
        parentNode: Union[None, str]=None,
    ):
        super().__init__()
        
        self.definition = definition
        self.parentNode = parentNode
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryNodeInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.definition = str()
        self.parentNode = self.RECORD_SCHEMA.field_map["parentNode"].default
    
    
    @property
    def definition(self) -> str:
        """Getter: Definition of business node"""
        return self._inner_dict.get('definition')  # type: ignore
    
    
    @definition.setter
    def definition(self, value: str) -> None:
        """Setter: Definition of business node"""
        self._inner_dict['definition'] = value
    
    
    @property
    def parentNode(self) -> Union[None, str]:
        """Getter: Parent node of the glossary term"""
        return self._inner_dict.get('parentNode')  # type: ignore
    
    
    @parentNode.setter
    def parentNode(self, value: Union[None, str]) -> None:
        """Setter: Parent node of the glossary term"""
        self._inner_dict['parentNode'] = value
    
    
class GlossaryTermInfoClass(DictWrapper):
    """Properties associated with a GlossaryTerm"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.glossary.GlossaryTermInfo")
    def __init__(self,
        definition: str,
        termSource: str,
        parentNode: Union[None, str]=None,
        sourceRef: Union[None, str]=None,
        sourceUrl: Union[None, str]=None,
        customProperties: Optional[Dict[str, str]]=None,
    ):
        super().__init__()
        
        self.definition = definition
        self.parentNode = parentNode
        self.termSource = termSource
        self.sourceRef = sourceRef
        self.sourceUrl = sourceUrl
        if customProperties is None:
            self.customProperties = {}
        else:
            self.customProperties = customProperties
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryTermInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.definition = str()
        self.parentNode = self.RECORD_SCHEMA.field_map["parentNode"].default
        self.termSource = str()
        self.sourceRef = self.RECORD_SCHEMA.field_map["sourceRef"].default
        self.sourceUrl = self.RECORD_SCHEMA.field_map["sourceUrl"].default
        self.customProperties = dict()
    
    
    @property
    def definition(self) -> str:
        """Getter: Definition of business term"""
        return self._inner_dict.get('definition')  # type: ignore
    
    
    @definition.setter
    def definition(self, value: str) -> None:
        """Setter: Definition of business term"""
        self._inner_dict['definition'] = value
    
    
    @property
    def parentNode(self) -> Union[None, str]:
        """Getter: Parent node of the glossary term"""
        return self._inner_dict.get('parentNode')  # type: ignore
    
    
    @parentNode.setter
    def parentNode(self, value: Union[None, str]) -> None:
        """Setter: Parent node of the glossary term"""
        self._inner_dict['parentNode'] = value
    
    
    @property
    def termSource(self) -> str:
        """Getter: Source of the Business Term (INTERNAL or EXTERNAL) with default value as INTERNAL"""
        return self._inner_dict.get('termSource')  # type: ignore
    
    
    @termSource.setter
    def termSource(self, value: str) -> None:
        """Setter: Source of the Business Term (INTERNAL or EXTERNAL) with default value as INTERNAL"""
        self._inner_dict['termSource'] = value
    
    
    @property
    def sourceRef(self) -> Union[None, str]:
        """Getter: External Reference to the business-term"""
        return self._inner_dict.get('sourceRef')  # type: ignore
    
    
    @sourceRef.setter
    def sourceRef(self, value: Union[None, str]) -> None:
        """Setter: External Reference to the business-term"""
        self._inner_dict['sourceRef'] = value
    
    
    @property
    def sourceUrl(self) -> Union[None, str]:
        """Getter: The abstracted URL such as https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/CashInstrument."""
        return self._inner_dict.get('sourceUrl')  # type: ignore
    
    
    @sourceUrl.setter
    def sourceUrl(self, value: Union[None, str]) -> None:
        """Setter: The abstracted URL such as https://spec.edmcouncil.org/fibo/ontology/FBC/FinancialInstruments/FinancialInstruments/CashInstrument."""
        self._inner_dict['sourceUrl'] = value
    
    
    @property
    def customProperties(self) -> Dict[str, str]:
        """Getter: A key-value map to capture any other non-standardized properties for the glossary term"""
        return self._inner_dict.get('customProperties')  # type: ignore
    
    
    @customProperties.setter
    def customProperties(self, value: Dict[str, str]) -> None:
        """Setter: A key-value map to capture any other non-standardized properties for the glossary term"""
        self._inner_dict['customProperties'] = value
    
    
class CorpGroupInfoClass(DictWrapper):
    """group of corpUser, it may contains nested group"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.identity.CorpGroupInfo")
    def __init__(self,
        email: str,
        admins: List[str],
        members: List[str],
        groups: List[str],
    ):
        super().__init__()
        
        self.email = email
        self.admins = admins
        self.members = members
        self.groups = groups
    
    @classmethod
    def construct_with_defaults(cls) -> "CorpGroupInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.email = str()
        self.admins = list()
        self.members = list()
        self.groups = list()
    
    
    @property
    def email(self) -> str:
        """Getter: email of this group"""
        return self._inner_dict.get('email')  # type: ignore
    
    
    @email.setter
    def email(self, value: str) -> None:
        """Setter: email of this group"""
        self._inner_dict['email'] = value
    
    
    @property
    def admins(self) -> List[str]:
        """Getter: owners of this group"""
        return self._inner_dict.get('admins')  # type: ignore
    
    
    @admins.setter
    def admins(self, value: List[str]) -> None:
        """Setter: owners of this group"""
        self._inner_dict['admins'] = value
    
    
    @property
    def members(self) -> List[str]:
        """Getter: List of ldap urn in this group."""
        return self._inner_dict.get('members')  # type: ignore
    
    
    @members.setter
    def members(self, value: List[str]) -> None:
        """Setter: List of ldap urn in this group."""
        self._inner_dict['members'] = value
    
    
    @property
    def groups(self) -> List[str]:
        """Getter: List of groups in this group."""
        return self._inner_dict.get('groups')  # type: ignore
    
    
    @groups.setter
    def groups(self, value: List[str]) -> None:
        """Setter: List of groups in this group."""
        self._inner_dict['groups'] = value
    
    
class CorpUserEditableInfoClass(DictWrapper):
    """Linkedin corp user information that can be edited from UI"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.identity.CorpUserEditableInfo")
    def __init__(self,
        aboutMe: Union[None, str]=None,
        teams: Optional[List[str]]=None,
        skills: Optional[List[str]]=None,
        pictureLink: Optional[str]=None,
    ):
        super().__init__()
        
        self.aboutMe = aboutMe
        if teams is None:
            self.teams = []
        else:
            self.teams = teams
        if skills is None:
            self.skills = []
        else:
            self.skills = skills
        if pictureLink is None:
            self.pictureLink = 'https://raw.githubusercontent.com/linkedin/datahub/master/datahub-web/packages/data-portal/public/assets/images/default_avatar.png'
        else:
            self.pictureLink = pictureLink
    
    @classmethod
    def construct_with_defaults(cls) -> "CorpUserEditableInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.aboutMe = self.RECORD_SCHEMA.field_map["aboutMe"].default
        self.teams = list()
        self.skills = list()
        self.pictureLink = self.RECORD_SCHEMA.field_map["pictureLink"].default
    
    
    @property
    def aboutMe(self) -> Union[None, str]:
        """Getter: About me section of the user"""
        return self._inner_dict.get('aboutMe')  # type: ignore
    
    
    @aboutMe.setter
    def aboutMe(self, value: Union[None, str]) -> None:
        """Setter: About me section of the user"""
        self._inner_dict['aboutMe'] = value
    
    
    @property
    def teams(self) -> List[str]:
        """Getter: Teams that the user belongs to e.g. Metadata"""
        return self._inner_dict.get('teams')  # type: ignore
    
    
    @teams.setter
    def teams(self, value: List[str]) -> None:
        """Setter: Teams that the user belongs to e.g. Metadata"""
        self._inner_dict['teams'] = value
    
    
    @property
    def skills(self) -> List[str]:
        """Getter: Skills that the user possesses e.g. Machine Learning"""
        return self._inner_dict.get('skills')  # type: ignore
    
    
    @skills.setter
    def skills(self, value: List[str]) -> None:
        """Setter: Skills that the user possesses e.g. Machine Learning"""
        self._inner_dict['skills'] = value
    
    
    @property
    def pictureLink(self) -> str:
        """Getter: A URL which points to a picture which user wants to set as a profile photo"""
        return self._inner_dict.get('pictureLink')  # type: ignore
    
    
    @pictureLink.setter
    def pictureLink(self, value: str) -> None:
        """Setter: A URL which points to a picture which user wants to set as a profile photo"""
        self._inner_dict['pictureLink'] = value
    
    
class CorpUserInfoClass(DictWrapper):
    """Linkedin corp user information"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.identity.CorpUserInfo")
    def __init__(self,
        active: bool,
        email: str,
        displayName: Union[None, str]=None,
        title: Union[None, str]=None,
        managerUrn: Union[None, str]=None,
        departmentId: Union[None, int]=None,
        departmentName: Union[None, str]=None,
        firstName: Union[None, str]=None,
        lastName: Union[None, str]=None,
        fullName: Union[None, str]=None,
        countryCode: Union[None, str]=None,
    ):
        super().__init__()
        
        self.active = active
        self.displayName = displayName
        self.email = email
        self.title = title
        self.managerUrn = managerUrn
        self.departmentId = departmentId
        self.departmentName = departmentName
        self.firstName = firstName
        self.lastName = lastName
        self.fullName = fullName
        self.countryCode = countryCode
    
    @classmethod
    def construct_with_defaults(cls) -> "CorpUserInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.active = bool()
        self.displayName = self.RECORD_SCHEMA.field_map["displayName"].default
        self.email = str()
        self.title = self.RECORD_SCHEMA.field_map["title"].default
        self.managerUrn = self.RECORD_SCHEMA.field_map["managerUrn"].default
        self.departmentId = self.RECORD_SCHEMA.field_map["departmentId"].default
        self.departmentName = self.RECORD_SCHEMA.field_map["departmentName"].default
        self.firstName = self.RECORD_SCHEMA.field_map["firstName"].default
        self.lastName = self.RECORD_SCHEMA.field_map["lastName"].default
        self.fullName = self.RECORD_SCHEMA.field_map["fullName"].default
        self.countryCode = self.RECORD_SCHEMA.field_map["countryCode"].default
    
    
    @property
    def active(self) -> bool:
        """Getter: Whether the corpUser is active, ref: https://iwww.corp.linkedin.com/wiki/cf/display/GTSD/Accessing+Active+Directory+via+LDAP+tools"""
        return self._inner_dict.get('active')  # type: ignore
    
    
    @active.setter
    def active(self, value: bool) -> None:
        """Setter: Whether the corpUser is active, ref: https://iwww.corp.linkedin.com/wiki/cf/display/GTSD/Accessing+Active+Directory+via+LDAP+tools"""
        self._inner_dict['active'] = value
    
    
    @property
    def displayName(self) -> Union[None, str]:
        """Getter: displayName of this user ,  e.g.  Hang Zhang(DataHQ)"""
        return self._inner_dict.get('displayName')  # type: ignore
    
    
    @displayName.setter
    def displayName(self, value: Union[None, str]) -> None:
        """Setter: displayName of this user ,  e.g.  Hang Zhang(DataHQ)"""
        self._inner_dict['displayName'] = value
    
    
    @property
    def email(self) -> str:
        """Getter: email address of this user"""
        return self._inner_dict.get('email')  # type: ignore
    
    
    @email.setter
    def email(self, value: str) -> None:
        """Setter: email address of this user"""
        self._inner_dict['email'] = value
    
    
    @property
    def title(self) -> Union[None, str]:
        """Getter: title of this user"""
        return self._inner_dict.get('title')  # type: ignore
    
    
    @title.setter
    def title(self, value: Union[None, str]) -> None:
        """Setter: title of this user"""
        self._inner_dict['title'] = value
    
    
    @property
    def managerUrn(self) -> Union[None, str]:
        """Getter: direct manager of this user"""
        return self._inner_dict.get('managerUrn')  # type: ignore
    
    
    @managerUrn.setter
    def managerUrn(self, value: Union[None, str]) -> None:
        """Setter: direct manager of this user"""
        self._inner_dict['managerUrn'] = value
    
    
    @property
    def departmentId(self) -> Union[None, int]:
        """Getter: department id this user belong to"""
        return self._inner_dict.get('departmentId')  # type: ignore
    
    
    @departmentId.setter
    def departmentId(self, value: Union[None, int]) -> None:
        """Setter: department id this user belong to"""
        self._inner_dict['departmentId'] = value
    
    
    @property
    def departmentName(self) -> Union[None, str]:
        """Getter: department name this user belong to"""
        return self._inner_dict.get('departmentName')  # type: ignore
    
    
    @departmentName.setter
    def departmentName(self, value: Union[None, str]) -> None:
        """Setter: department name this user belong to"""
        self._inner_dict['departmentName'] = value
    
    
    @property
    def firstName(self) -> Union[None, str]:
        """Getter: first name of this user"""
        return self._inner_dict.get('firstName')  # type: ignore
    
    
    @firstName.setter
    def firstName(self, value: Union[None, str]) -> None:
        """Setter: first name of this user"""
        self._inner_dict['firstName'] = value
    
    
    @property
    def lastName(self) -> Union[None, str]:
        """Getter: last name of this user"""
        return self._inner_dict.get('lastName')  # type: ignore
    
    
    @lastName.setter
    def lastName(self, value: Union[None, str]) -> None:
        """Setter: last name of this user"""
        self._inner_dict['lastName'] = value
    
    
    @property
    def fullName(self) -> Union[None, str]:
        """Getter: Common name of this user, format is firstName + lastName (split by a whitespace)"""
        return self._inner_dict.get('fullName')  # type: ignore
    
    
    @fullName.setter
    def fullName(self, value: Union[None, str]) -> None:
        """Setter: Common name of this user, format is firstName + lastName (split by a whitespace)"""
        self._inner_dict['fullName'] = value
    
    
    @property
    def countryCode(self) -> Union[None, str]:
        """Getter: two uppercase letters country code. e.g.  US"""
        return self._inner_dict.get('countryCode')  # type: ignore
    
    
    @countryCode.setter
    def countryCode(self, value: Union[None, str]) -> None:
        """Setter: two uppercase letters country code. e.g.  US"""
        self._inner_dict['countryCode'] = value
    
    
class ChartSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific Chart entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.ChartSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["ChartInfoClass", "ChartQueryClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "ChartSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["ChartInfoClass", "ChartQueryClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the chart. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["ChartInfoClass", "ChartQueryClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the chart. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class CorpGroupSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific CorpGroup entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.CorpGroupSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["CorpGroupInfoClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "CorpGroupSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["CorpGroupInfoClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the LdapUser. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["CorpGroupInfoClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the LdapUser. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class CorpUserSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific CorpUser entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.CorpUserSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["CorpUserInfoClass", "CorpUserEditableInfoClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "CorpUserSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["CorpUserInfoClass", "CorpUserEditableInfoClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the CorpUser. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["CorpUserInfoClass", "CorpUserEditableInfoClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the CorpUser. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class DashboardSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific Dashboard entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.DashboardSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["DashboardInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "DashboardSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["DashboardInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the dashboard. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["DashboardInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the dashboard. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class DataFlowSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific DataFlow entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.DataFlowSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["DataFlowInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "DataFlowSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["DataFlowInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the data flow. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["DataFlowInfoClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the data flow. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class DataJobSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific DataJob entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.DataJobSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["DataJobInfoClass", "DataJobInputOutputClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "DataJobSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["DataJobInfoClass", "DataJobInputOutputClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]:
        """Getter: The list of metadata aspects associated with the data job. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["DataJobInfoClass", "DataJobInputOutputClass", "OwnershipClass", "StatusClass", "GlobalTagsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the data job. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class DataProcessSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific Data process entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.DataProcessSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["OwnershipClass", "DataProcessInfoClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "DataProcessSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["OwnershipClass", "DataProcessInfoClass"]]:
        """Getter: The list of metadata aspects associated with the data process. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["OwnershipClass", "DataProcessInfoClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the data process. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class DatasetSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific dataset entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["DatasetPropertiesClass", "DatasetDeprecationClass", "DatasetUpstreamLineageClass", "UpstreamLineageClass", "InstitutionalMemoryClass", "OwnershipClass", "StatusClass", "SchemaMetadataClass", "EditableSchemaMetadataClass", "GlobalTagsClass", "GlossaryTermsClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["DatasetPropertiesClass", "DatasetDeprecationClass", "DatasetUpstreamLineageClass", "UpstreamLineageClass", "InstitutionalMemoryClass", "OwnershipClass", "StatusClass", "SchemaMetadataClass", "EditableSchemaMetadataClass", "GlobalTagsClass", "GlossaryTermsClass"]]:
        """Getter: The list of metadata aspects associated with the dataset. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["DatasetPropertiesClass", "DatasetDeprecationClass", "DatasetUpstreamLineageClass", "UpstreamLineageClass", "InstitutionalMemoryClass", "OwnershipClass", "StatusClass", "SchemaMetadataClass", "EditableSchemaMetadataClass", "GlobalTagsClass", "GlossaryTermsClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the dataset. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class GlossaryNodeSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific GlossaryNode entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.GlossaryNodeSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["GlossaryNodeInfoClass", "OwnershipClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryNodeSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["GlossaryNodeInfoClass", "OwnershipClass"]]:
        """Getter: The list of metadata aspects associated with the GlossaryNode. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["GlossaryNodeInfoClass", "OwnershipClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the GlossaryNode. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class GlossaryTermSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific GlossaryTerm entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.GlossaryTermSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["GlossaryTermInfoClass", "OwnershipClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "GlossaryTermSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["GlossaryTermInfoClass", "OwnershipClass"]]:
        """Getter: The list of metadata aspects associated with the GlossaryTerm. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["GlossaryTermInfoClass", "OwnershipClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the GlossaryTerm. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class MLFeatureSnapshotClass(DictWrapper):
    # No docs available.
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.MLFeatureSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["OwnershipClass", "MLFeaturePropertiesClass", "InstitutionalMemoryClass", "StatusClass", "DeprecationClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "MLFeatureSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["OwnershipClass", "MLFeaturePropertiesClass", "InstitutionalMemoryClass", "StatusClass", "DeprecationClass"]]:
        """Getter: The list of metadata aspects associated with the MLModel. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["OwnershipClass", "MLFeaturePropertiesClass", "InstitutionalMemoryClass", "StatusClass", "DeprecationClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the MLModel. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class MLModelSnapshotClass(DictWrapper):
    """MLModel Snapshot entity details."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.MLModelSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["OwnershipClass", "MLModelPropertiesClass", "IntendedUseClass", "MLModelFactorPromptsClass", "MetricsClass", "EvaluationDataClass", "TrainingDataClass", "QuantitativeAnalysesClass", "EthicalConsiderationsClass", "CaveatsAndRecommendationsClass", "InstitutionalMemoryClass", "SourceCodeClass", "StatusClass", "CostClass", "DeprecationClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "MLModelSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["OwnershipClass", "MLModelPropertiesClass", "IntendedUseClass", "MLModelFactorPromptsClass", "MetricsClass", "EvaluationDataClass", "TrainingDataClass", "QuantitativeAnalysesClass", "EthicalConsiderationsClass", "CaveatsAndRecommendationsClass", "InstitutionalMemoryClass", "SourceCodeClass", "StatusClass", "CostClass", "DeprecationClass"]]:
        """Getter: The list of metadata aspects associated with the MLModel. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["OwnershipClass", "MLModelPropertiesClass", "IntendedUseClass", "MLModelFactorPromptsClass", "MetricsClass", "EvaluationDataClass", "TrainingDataClass", "QuantitativeAnalysesClass", "EthicalConsiderationsClass", "CaveatsAndRecommendationsClass", "InstitutionalMemoryClass", "SourceCodeClass", "StatusClass", "CostClass", "DeprecationClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the MLModel. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class TagSnapshotClass(DictWrapper):
    """A metadata snapshot for a specific dataset entity."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.metadata.snapshot.TagSnapshot")
    def __init__(self,
        urn: str,
        aspects: List[Union["OwnershipClass", "TagPropertiesClass"]],
    ):
        super().__init__()
        
        self.urn = urn
        self.aspects = aspects
    
    @classmethod
    def construct_with_defaults(cls) -> "TagSnapshotClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.urn = str()
        self.aspects = list()
    
    
    @property
    def urn(self) -> str:
        """Getter: URN for the entity the metadata snapshot is associated with."""
        return self._inner_dict.get('urn')  # type: ignore
    
    
    @urn.setter
    def urn(self, value: str) -> None:
        """Setter: URN for the entity the metadata snapshot is associated with."""
        self._inner_dict['urn'] = value
    
    
    @property
    def aspects(self) -> List[Union["OwnershipClass", "TagPropertiesClass"]]:
        """Getter: The list of metadata aspects associated with the dataset. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        return self._inner_dict.get('aspects')  # type: ignore
    
    
    @aspects.setter
    def aspects(self, value: List[Union["OwnershipClass", "TagPropertiesClass"]]) -> None:
        """Setter: The list of metadata aspects associated with the dataset. Depending on the use case, this can either be all, or a selection, of supported aspects."""
        self._inner_dict['aspects'] = value
    
    
class BaseDataClass(DictWrapper):
    """BaseData record"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.BaseData")
    def __init__(self,
        dataset: str,
        motivation: Union[None, str]=None,
        preProcessing: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.dataset = dataset
        self.motivation = motivation
        self.preProcessing = preProcessing
    
    @classmethod
    def construct_with_defaults(cls) -> "BaseDataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.dataset = str()
        self.motivation = self.RECORD_SCHEMA.field_map["motivation"].default
        self.preProcessing = self.RECORD_SCHEMA.field_map["preProcessing"].default
    
    
    @property
    def dataset(self) -> str:
        """Getter: What dataset were used in the MLModel?"""
        return self._inner_dict.get('dataset')  # type: ignore
    
    
    @dataset.setter
    def dataset(self, value: str) -> None:
        """Setter: What dataset were used in the MLModel?"""
        self._inner_dict['dataset'] = value
    
    
    @property
    def motivation(self) -> Union[None, str]:
        """Getter: Why was this dataset chosen?"""
        return self._inner_dict.get('motivation')  # type: ignore
    
    
    @motivation.setter
    def motivation(self, value: Union[None, str]) -> None:
        """Setter: Why was this dataset chosen?"""
        self._inner_dict['motivation'] = value
    
    
    @property
    def preProcessing(self) -> Union[None, List[str]]:
        """Getter: How was the data preprocessed (e.g., tokenization of sentences, cropping of images, any filtering such as dropping images without faces)?"""
        return self._inner_dict.get('preProcessing')  # type: ignore
    
    
    @preProcessing.setter
    def preProcessing(self, value: Union[None, List[str]]) -> None:
        """Setter: How was the data preprocessed (e.g., tokenization of sentences, cropping of images, any filtering such as dropping images without faces)?"""
        self._inner_dict['preProcessing'] = value
    
    
class CaveatDetailsClass(DictWrapper):
    """This section should list additional concerns that were not covered in the previous sections. For example, did the results suggest any further testing? Were there any relevant groups that were not represented in the evaluation dataset? Are there additional recommendations for model use?"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.CaveatDetails")
    def __init__(self,
        needsFurtherTesting: Union[None, bool]=None,
        caveatDescription: Union[None, str]=None,
        groupsNotRepresented: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.needsFurtherTesting = needsFurtherTesting
        self.caveatDescription = caveatDescription
        self.groupsNotRepresented = groupsNotRepresented
    
    @classmethod
    def construct_with_defaults(cls) -> "CaveatDetailsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.needsFurtherTesting = self.RECORD_SCHEMA.field_map["needsFurtherTesting"].default
        self.caveatDescription = self.RECORD_SCHEMA.field_map["caveatDescription"].default
        self.groupsNotRepresented = self.RECORD_SCHEMA.field_map["groupsNotRepresented"].default
    
    
    @property
    def needsFurtherTesting(self) -> Union[None, bool]:
        """Getter: Did the results suggest any further testing?"""
        return self._inner_dict.get('needsFurtherTesting')  # type: ignore
    
    
    @needsFurtherTesting.setter
    def needsFurtherTesting(self, value: Union[None, bool]) -> None:
        """Setter: Did the results suggest any further testing?"""
        self._inner_dict['needsFurtherTesting'] = value
    
    
    @property
    def caveatDescription(self) -> Union[None, str]:
        """Getter: Caveat Description
    For ex: Given gender classes are binary (male/not male), which we include as male/female. Further work needed to evaluate across a spectrum of genders."""
        return self._inner_dict.get('caveatDescription')  # type: ignore
    
    
    @caveatDescription.setter
    def caveatDescription(self, value: Union[None, str]) -> None:
        """Setter: Caveat Description
    For ex: Given gender classes are binary (male/not male), which we include as male/female. Further work needed to evaluate across a spectrum of genders."""
        self._inner_dict['caveatDescription'] = value
    
    
    @property
    def groupsNotRepresented(self) -> Union[None, List[str]]:
        """Getter: Relevant groups that were not represented in the evaluation dataset?"""
        return self._inner_dict.get('groupsNotRepresented')  # type: ignore
    
    
    @groupsNotRepresented.setter
    def groupsNotRepresented(self, value: Union[None, List[str]]) -> None:
        """Setter: Relevant groups that were not represented in the evaluation dataset?"""
        self._inner_dict['groupsNotRepresented'] = value
    
    
class CaveatsAndRecommendationsClass(DictWrapper):
    """This section should list additional concerns that were not covered in the previous sections. For example, did the results suggest any further testing? Were there any relevant groups that were not represented in the evaluation dataset? Are there additional recommendations for model use?"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.CaveatsAndRecommendations")
    def __init__(self,
        caveats: Union[None, "CaveatDetailsClass"]=None,
        recommendations: Union[None, str]=None,
        idealDatasetCharacteristics: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.caveats = caveats
        self.recommendations = recommendations
        self.idealDatasetCharacteristics = idealDatasetCharacteristics
    
    @classmethod
    def construct_with_defaults(cls) -> "CaveatsAndRecommendationsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.caveats = self.RECORD_SCHEMA.field_map["caveats"].default
        self.recommendations = self.RECORD_SCHEMA.field_map["recommendations"].default
        self.idealDatasetCharacteristics = self.RECORD_SCHEMA.field_map["idealDatasetCharacteristics"].default
    
    
    @property
    def caveats(self) -> Union[None, "CaveatDetailsClass"]:
        """Getter: This section should list additional concerns that were not covered in the previous sections. For example, did the results suggest any further testing? Were there any relevant groups that were not represented in the evaluation dataset?"""
        return self._inner_dict.get('caveats')  # type: ignore
    
    
    @caveats.setter
    def caveats(self, value: Union[None, "CaveatDetailsClass"]) -> None:
        """Setter: This section should list additional concerns that were not covered in the previous sections. For example, did the results suggest any further testing? Were there any relevant groups that were not represented in the evaluation dataset?"""
        self._inner_dict['caveats'] = value
    
    
    @property
    def recommendations(self) -> Union[None, str]:
        """Getter: Recommendations on where this MLModel should be used."""
        return self._inner_dict.get('recommendations')  # type: ignore
    
    
    @recommendations.setter
    def recommendations(self, value: Union[None, str]) -> None:
        """Setter: Recommendations on where this MLModel should be used."""
        self._inner_dict['recommendations'] = value
    
    
    @property
    def idealDatasetCharacteristics(self) -> Union[None, List[str]]:
        """Getter: Ideal characteristics of an evaluation dataset for this MLModel"""
        return self._inner_dict.get('idealDatasetCharacteristics')  # type: ignore
    
    
    @idealDatasetCharacteristics.setter
    def idealDatasetCharacteristics(self, value: Union[None, List[str]]) -> None:
        """Setter: Ideal characteristics of an evaluation dataset for this MLModel"""
        self._inner_dict['idealDatasetCharacteristics'] = value
    
    
class EthicalConsiderationsClass(DictWrapper):
    """This section is intended to demonstrate the ethical considerations that went into MLModel development, surfacing ethical challenges and solutions to stakeholders."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.EthicalConsiderations")
    def __init__(self,
        data: Union[None, List[str]]=None,
        humanLife: Union[None, List[str]]=None,
        mitigations: Union[None, List[str]]=None,
        risksAndHarms: Union[None, List[str]]=None,
        useCases: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.data = data
        self.humanLife = humanLife
        self.mitigations = mitigations
        self.risksAndHarms = risksAndHarms
        self.useCases = useCases
    
    @classmethod
    def construct_with_defaults(cls) -> "EthicalConsiderationsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.data = self.RECORD_SCHEMA.field_map["data"].default
        self.humanLife = self.RECORD_SCHEMA.field_map["humanLife"].default
        self.mitigations = self.RECORD_SCHEMA.field_map["mitigations"].default
        self.risksAndHarms = self.RECORD_SCHEMA.field_map["risksAndHarms"].default
        self.useCases = self.RECORD_SCHEMA.field_map["useCases"].default
    
    
    @property
    def data(self) -> Union[None, List[str]]:
        """Getter: Does the MLModel use any sensitive data (e.g., protected classes)?"""
        return self._inner_dict.get('data')  # type: ignore
    
    
    @data.setter
    def data(self, value: Union[None, List[str]]) -> None:
        """Setter: Does the MLModel use any sensitive data (e.g., protected classes)?"""
        self._inner_dict['data'] = value
    
    
    @property
    def humanLife(self) -> Union[None, List[str]]:
        """Getter:  Is the MLModel intended to inform decisions about matters central to human life or flourishing – e.g., health or safety? Or could it be used in such a way?"""
        return self._inner_dict.get('humanLife')  # type: ignore
    
    
    @humanLife.setter
    def humanLife(self, value: Union[None, List[str]]) -> None:
        """Setter:  Is the MLModel intended to inform decisions about matters central to human life or flourishing – e.g., health or safety? Or could it be used in such a way?"""
        self._inner_dict['humanLife'] = value
    
    
    @property
    def mitigations(self) -> Union[None, List[str]]:
        """Getter: What risk mitigation strategies were used during MLModel development?"""
        return self._inner_dict.get('mitigations')  # type: ignore
    
    
    @mitigations.setter
    def mitigations(self, value: Union[None, List[str]]) -> None:
        """Setter: What risk mitigation strategies were used during MLModel development?"""
        self._inner_dict['mitigations'] = value
    
    
    @property
    def risksAndHarms(self) -> Union[None, List[str]]:
        """Getter: What risks may be present in MLModel usage? Try to identify the potential recipients, likelihood, and magnitude of harms. If these cannot be determined, note that they were considered but remain unknown."""
        return self._inner_dict.get('risksAndHarms')  # type: ignore
    
    
    @risksAndHarms.setter
    def risksAndHarms(self, value: Union[None, List[str]]) -> None:
        """Setter: What risks may be present in MLModel usage? Try to identify the potential recipients, likelihood, and magnitude of harms. If these cannot be determined, note that they were considered but remain unknown."""
        self._inner_dict['risksAndHarms'] = value
    
    
    @property
    def useCases(self) -> Union[None, List[str]]:
        """Getter: Are there any known MLModel use cases that are especially fraught? This may connect directly to the intended use section"""
        return self._inner_dict.get('useCases')  # type: ignore
    
    
    @useCases.setter
    def useCases(self, value: Union[None, List[str]]) -> None:
        """Setter: Are there any known MLModel use cases that are especially fraught? This may connect directly to the intended use section"""
        self._inner_dict['useCases'] = value
    
    
class EvaluationDataClass(DictWrapper):
    """All referenced datasets would ideally point to any set of documents that provide visibility into the source and composition of the dataset."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.EvaluationData")
    def __init__(self,
        evaluationData: List["BaseDataClass"],
    ):
        super().__init__()
        
        self.evaluationData = evaluationData
    
    @classmethod
    def construct_with_defaults(cls) -> "EvaluationDataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.evaluationData = list()
    
    
    @property
    def evaluationData(self) -> List["BaseDataClass"]:
        """Getter: Details on the dataset(s) used for the quantitative analyses in the MLModel"""
        return self._inner_dict.get('evaluationData')  # type: ignore
    
    
    @evaluationData.setter
    def evaluationData(self, value: List["BaseDataClass"]) -> None:
        """Setter: Details on the dataset(s) used for the quantitative analyses in the MLModel"""
        self._inner_dict['evaluationData'] = value
    
    
class IntendedUseClass(DictWrapper):
    """Intended Use for the ML Model"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.IntendedUse")
    def __init__(self,
        primaryUses: Union[None, List[str]]=None,
        primaryUsers: Union[None, List[Union[str, "IntendedUserTypeClass"]]]=None,
        outOfScopeUses: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.primaryUses = primaryUses
        self.primaryUsers = primaryUsers
        self.outOfScopeUses = outOfScopeUses
    
    @classmethod
    def construct_with_defaults(cls) -> "IntendedUseClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.primaryUses = self.RECORD_SCHEMA.field_map["primaryUses"].default
        self.primaryUsers = self.RECORD_SCHEMA.field_map["primaryUsers"].default
        self.outOfScopeUses = self.RECORD_SCHEMA.field_map["outOfScopeUses"].default
    
    
    @property
    def primaryUses(self) -> Union[None, List[str]]:
        """Getter: Primary Use cases for the MLModel."""
        return self._inner_dict.get('primaryUses')  # type: ignore
    
    
    @primaryUses.setter
    def primaryUses(self, value: Union[None, List[str]]) -> None:
        """Setter: Primary Use cases for the MLModel."""
        self._inner_dict['primaryUses'] = value
    
    
    @property
    def primaryUsers(self) -> Union[None, List[Union[str, "IntendedUserTypeClass"]]]:
        """Getter: Primary Intended Users - For example, was the MLModel developed for entertainment purposes, for hobbyists, or enterprise solutions?"""
        return self._inner_dict.get('primaryUsers')  # type: ignore
    
    
    @primaryUsers.setter
    def primaryUsers(self, value: Union[None, List[Union[str, "IntendedUserTypeClass"]]]) -> None:
        """Setter: Primary Intended Users - For example, was the MLModel developed for entertainment purposes, for hobbyists, or enterprise solutions?"""
        self._inner_dict['primaryUsers'] = value
    
    
    @property
    def outOfScopeUses(self) -> Union[None, List[str]]:
        """Getter: Highlight technology that the MLModel might easily be confused with, or related contexts that users could try to apply the MLModel to."""
        return self._inner_dict.get('outOfScopeUses')  # type: ignore
    
    
    @outOfScopeUses.setter
    def outOfScopeUses(self, value: Union[None, List[str]]) -> None:
        """Setter: Highlight technology that the MLModel might easily be confused with, or related contexts that users could try to apply the MLModel to."""
        self._inner_dict['outOfScopeUses'] = value
    
    
class IntendedUserTypeClass(object):
    # No docs available.
    
    ENTERPRISE = "ENTERPRISE"
    HOBBY = "HOBBY"
    ENTERTAINMENT = "ENTERTAINMENT"
    
    
class MLFeaturePropertiesClass(DictWrapper):
    """Properties associated with a MLFeature"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.MLFeatureProperties")
    def __init__(self,
        description: Union[None, str]=None,
        dataType: Union[None, Union[str, "MLFeatureDataTypeClass"]]=None,
        version: Union[None, "VersionTagClass"]=None,
    ):
        super().__init__()
        
        self.description = description
        self.dataType = dataType
        self.version = version
    
    @classmethod
    def construct_with_defaults(cls) -> "MLFeaturePropertiesClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.dataType = self.RECORD_SCHEMA.field_map["dataType"].default
        self.version = self.RECORD_SCHEMA.field_map["version"].default
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Documentation of the MLFeature"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Documentation of the MLFeature"""
        self._inner_dict['description'] = value
    
    
    @property
    def dataType(self) -> Union[None, Union[str, "MLFeatureDataTypeClass"]]:
        """Getter: Data Type of the MLFeature"""
        return self._inner_dict.get('dataType')  # type: ignore
    
    
    @dataType.setter
    def dataType(self, value: Union[None, Union[str, "MLFeatureDataTypeClass"]]) -> None:
        """Setter: Data Type of the MLFeature"""
        self._inner_dict['dataType'] = value
    
    
    @property
    def version(self) -> Union[None, "VersionTagClass"]:
        """Getter: Version of the MLFeature"""
        return self._inner_dict.get('version')  # type: ignore
    
    
    @version.setter
    def version(self, value: Union[None, "VersionTagClass"]) -> None:
        """Setter: Version of the MLFeature"""
        self._inner_dict['version'] = value
    
    
class MLModelFactorPromptsClass(DictWrapper):
    """Prompts which affect the performance of the MLModel"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.MLModelFactorPrompts")
    def __init__(self,
        relevantFactors: Union[None, List["MLModelFactorsClass"]]=None,
        evaluationFactors: Union[None, List["MLModelFactorsClass"]]=None,
    ):
        super().__init__()
        
        self.relevantFactors = relevantFactors
        self.evaluationFactors = evaluationFactors
    
    @classmethod
    def construct_with_defaults(cls) -> "MLModelFactorPromptsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.relevantFactors = self.RECORD_SCHEMA.field_map["relevantFactors"].default
        self.evaluationFactors = self.RECORD_SCHEMA.field_map["evaluationFactors"].default
    
    
    @property
    def relevantFactors(self) -> Union[None, List["MLModelFactorsClass"]]:
        """Getter: What are foreseeable salient factors for which MLModel performance may vary, and how were these determined?"""
        return self._inner_dict.get('relevantFactors')  # type: ignore
    
    
    @relevantFactors.setter
    def relevantFactors(self, value: Union[None, List["MLModelFactorsClass"]]) -> None:
        """Setter: What are foreseeable salient factors for which MLModel performance may vary, and how were these determined?"""
        self._inner_dict['relevantFactors'] = value
    
    
    @property
    def evaluationFactors(self) -> Union[None, List["MLModelFactorsClass"]]:
        """Getter: Which factors are being reported, and why were these chosen?"""
        return self._inner_dict.get('evaluationFactors')  # type: ignore
    
    
    @evaluationFactors.setter
    def evaluationFactors(self, value: Union[None, List["MLModelFactorsClass"]]) -> None:
        """Setter: Which factors are being reported, and why were these chosen?"""
        self._inner_dict['evaluationFactors'] = value
    
    
class MLModelFactorsClass(DictWrapper):
    """Factors affecting the performance of the MLModel."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.MLModelFactors")
    def __init__(self,
        groups: Union[None, List[str]]=None,
        instrumentation: Union[None, List[str]]=None,
        environment: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.groups = groups
        self.instrumentation = instrumentation
        self.environment = environment
    
    @classmethod
    def construct_with_defaults(cls) -> "MLModelFactorsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.groups = self.RECORD_SCHEMA.field_map["groups"].default
        self.instrumentation = self.RECORD_SCHEMA.field_map["instrumentation"].default
        self.environment = self.RECORD_SCHEMA.field_map["environment"].default
    
    
    @property
    def groups(self) -> Union[None, List[str]]:
        """Getter: Groups refers to distinct categories with similar characteristics that are present in the evaluation data instances.
    For human-centric machine learning MLModels, groups are people who share one or multiple characteristics."""
        return self._inner_dict.get('groups')  # type: ignore
    
    
    @groups.setter
    def groups(self, value: Union[None, List[str]]) -> None:
        """Setter: Groups refers to distinct categories with similar characteristics that are present in the evaluation data instances.
    For human-centric machine learning MLModels, groups are people who share one or multiple characteristics."""
        self._inner_dict['groups'] = value
    
    
    @property
    def instrumentation(self) -> Union[None, List[str]]:
        """Getter: The performance of a MLModel can vary depending on what instruments were used to capture the input to the MLModel.
    For example, a face detection model may perform differently depending on the camera’s hardware and software,
    including lens, image stabilization, high dynamic range techniques, and background blurring for portrait mode."""
        return self._inner_dict.get('instrumentation')  # type: ignore
    
    
    @instrumentation.setter
    def instrumentation(self, value: Union[None, List[str]]) -> None:
        """Setter: The performance of a MLModel can vary depending on what instruments were used to capture the input to the MLModel.
    For example, a face detection model may perform differently depending on the camera’s hardware and software,
    including lens, image stabilization, high dynamic range techniques, and background blurring for portrait mode."""
        self._inner_dict['instrumentation'] = value
    
    
    @property
    def environment(self) -> Union[None, List[str]]:
        """Getter: A further factor affecting MLModel performance is the environment in which it is deployed."""
        return self._inner_dict.get('environment')  # type: ignore
    
    
    @environment.setter
    def environment(self, value: Union[None, List[str]]) -> None:
        """Setter: A further factor affecting MLModel performance is the environment in which it is deployed."""
        self._inner_dict['environment'] = value
    
    
class MLModelPropertiesClass(DictWrapper):
    """Properties associated with a ML Model"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.MLModelProperties")
    def __init__(self,
        description: Union[None, str]=None,
        date: Union[None, int]=None,
        version: Union[None, "VersionTagClass"]=None,
        type: Union[None, str]=None,
        hyperParameters: Union[None, Dict[str, Union[str, int, float, float, bool]]]=None,
        mlFeatures: Union[None, List[str]]=None,
        tags: Optional[List[str]]=None,
    ):
        super().__init__()
        
        self.description = description
        self.date = date
        self.version = version
        self.type = type
        self.hyperParameters = hyperParameters
        self.mlFeatures = mlFeatures
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
    
    @classmethod
    def construct_with_defaults(cls) -> "MLModelPropertiesClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.date = self.RECORD_SCHEMA.field_map["date"].default
        self.version = self.RECORD_SCHEMA.field_map["version"].default
        self.type = self.RECORD_SCHEMA.field_map["type"].default
        self.hyperParameters = self.RECORD_SCHEMA.field_map["hyperParameters"].default
        self.mlFeatures = self.RECORD_SCHEMA.field_map["mlFeatures"].default
        self.tags = list()
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Documentation of the MLModel"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Documentation of the MLModel"""
        self._inner_dict['description'] = value
    
    
    @property
    def date(self) -> Union[None, int]:
        """Getter: Date when the MLModel was developed"""
        return self._inner_dict.get('date')  # type: ignore
    
    
    @date.setter
    def date(self, value: Union[None, int]) -> None:
        """Setter: Date when the MLModel was developed"""
        self._inner_dict['date'] = value
    
    
    @property
    def version(self) -> Union[None, "VersionTagClass"]:
        """Getter: Version of the MLModel"""
        return self._inner_dict.get('version')  # type: ignore
    
    
    @version.setter
    def version(self, value: Union[None, "VersionTagClass"]) -> None:
        """Setter: Version of the MLModel"""
        self._inner_dict['version'] = value
    
    
    @property
    def type(self) -> Union[None, str]:
        """Getter: Type of Algorithm or MLModel such as whether it is a Naive Bayes classifier, Convolutional Neural Network, etc"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[None, str]) -> None:
        """Setter: Type of Algorithm or MLModel such as whether it is a Naive Bayes classifier, Convolutional Neural Network, etc"""
        self._inner_dict['type'] = value
    
    
    @property
    def hyperParameters(self) -> Union[None, Dict[str, Union[str, int, float, float, bool]]]:
        """Getter: Hyper Parameters of the MLModel"""
        return self._inner_dict.get('hyperParameters')  # type: ignore
    
    
    @hyperParameters.setter
    def hyperParameters(self, value: Union[None, Dict[str, Union[str, int, float, float, bool]]]) -> None:
        """Setter: Hyper Parameters of the MLModel"""
        self._inner_dict['hyperParameters'] = value
    
    
    @property
    def mlFeatures(self) -> Union[None, List[str]]:
        """Getter: List of features used for MLModel training"""
        return self._inner_dict.get('mlFeatures')  # type: ignore
    
    
    @mlFeatures.setter
    def mlFeatures(self, value: Union[None, List[str]]) -> None:
        """Setter: List of features used for MLModel training"""
        self._inner_dict['mlFeatures'] = value
    
    
    @property
    def tags(self) -> List[str]:
        """Getter: Tags for the MLModel"""
        return self._inner_dict.get('tags')  # type: ignore
    
    
    @tags.setter
    def tags(self, value: List[str]) -> None:
        """Setter: Tags for the MLModel"""
        self._inner_dict['tags'] = value
    
    
class MetricsClass(DictWrapper):
    """Metrics to be featured for the MLModel."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.Metrics")
    def __init__(self,
        performanceMeasures: Union[None, List[str]]=None,
        decisionThreshold: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.performanceMeasures = performanceMeasures
        self.decisionThreshold = decisionThreshold
    
    @classmethod
    def construct_with_defaults(cls) -> "MetricsClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.performanceMeasures = self.RECORD_SCHEMA.field_map["performanceMeasures"].default
        self.decisionThreshold = self.RECORD_SCHEMA.field_map["decisionThreshold"].default
    
    
    @property
    def performanceMeasures(self) -> Union[None, List[str]]:
        """Getter: Measures of MLModel performance"""
        return self._inner_dict.get('performanceMeasures')  # type: ignore
    
    
    @performanceMeasures.setter
    def performanceMeasures(self, value: Union[None, List[str]]) -> None:
        """Setter: Measures of MLModel performance"""
        self._inner_dict['performanceMeasures'] = value
    
    
    @property
    def decisionThreshold(self) -> Union[None, List[str]]:
        """Getter: Decision Thresholds used (if any)?"""
        return self._inner_dict.get('decisionThreshold')  # type: ignore
    
    
    @decisionThreshold.setter
    def decisionThreshold(self, value: Union[None, List[str]]) -> None:
        """Setter: Decision Thresholds used (if any)?"""
        self._inner_dict['decisionThreshold'] = value
    
    
class QuantitativeAnalysesClass(DictWrapper):
    """Quantitative analyses should be disaggregated, that is, broken down by the chosen factors. Quantitative analyses should provide the results of evaluating the MLModel according to the chosen metrics, providing confidence interval values when possible."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.QuantitativeAnalyses")
    def __init__(self,
        unitaryResults: Union[None, str]=None,
        intersectionalResults: Union[None, str]=None,
    ):
        super().__init__()
        
        self.unitaryResults = unitaryResults
        self.intersectionalResults = intersectionalResults
    
    @classmethod
    def construct_with_defaults(cls) -> "QuantitativeAnalysesClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.unitaryResults = self.RECORD_SCHEMA.field_map["unitaryResults"].default
        self.intersectionalResults = self.RECORD_SCHEMA.field_map["intersectionalResults"].default
    
    
    @property
    def unitaryResults(self) -> Union[None, str]:
        """Getter: Link to a dashboard with results showing how the MLModel performed with respect to each factor"""
        return self._inner_dict.get('unitaryResults')  # type: ignore
    
    
    @unitaryResults.setter
    def unitaryResults(self, value: Union[None, str]) -> None:
        """Setter: Link to a dashboard with results showing how the MLModel performed with respect to each factor"""
        self._inner_dict['unitaryResults'] = value
    
    
    @property
    def intersectionalResults(self) -> Union[None, str]:
        """Getter: Link to a dashboard with results showing how the MLModel performed with respect to the intersection of evaluated factors?"""
        return self._inner_dict.get('intersectionalResults')  # type: ignore
    
    
    @intersectionalResults.setter
    def intersectionalResults(self, value: Union[None, str]) -> None:
        """Setter: Link to a dashboard with results showing how the MLModel performed with respect to the intersection of evaluated factors?"""
        self._inner_dict['intersectionalResults'] = value
    
    
class SourceCodeClass(DictWrapper):
    """Source Code"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.SourceCode")
    def __init__(self,
        sourceCode: List["SourceCodeUrlClass"],
    ):
        super().__init__()
        
        self.sourceCode = sourceCode
    
    @classmethod
    def construct_with_defaults(cls) -> "SourceCodeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.sourceCode = list()
    
    
    @property
    def sourceCode(self) -> List["SourceCodeUrlClass"]:
        """Getter: Source Code along with types"""
        return self._inner_dict.get('sourceCode')  # type: ignore
    
    
    @sourceCode.setter
    def sourceCode(self, value: List["SourceCodeUrlClass"]) -> None:
        """Setter: Source Code along with types"""
        self._inner_dict['sourceCode'] = value
    
    
class SourceCodeUrlClass(DictWrapper):
    """Source Code Url Entity"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.SourceCodeUrl")
    def __init__(self,
        type: Union[str, "SourceCodeUrlTypeClass"],
        sourceCodeUrl: str,
    ):
        super().__init__()
        
        self.type = type
        self.sourceCodeUrl = sourceCodeUrl
    
    @classmethod
    def construct_with_defaults(cls) -> "SourceCodeUrlClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.type = SourceCodeUrlTypeClass.ML_MODEL_SOURCE_CODE
        self.sourceCodeUrl = str()
    
    
    @property
    def type(self) -> Union[str, "SourceCodeUrlTypeClass"]:
        """Getter: Source Code Url Types"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union[str, "SourceCodeUrlTypeClass"]) -> None:
        """Setter: Source Code Url Types"""
        self._inner_dict['type'] = value
    
    
    @property
    def sourceCodeUrl(self) -> str:
        """Getter: Source Code Url"""
        return self._inner_dict.get('sourceCodeUrl')  # type: ignore
    
    
    @sourceCodeUrl.setter
    def sourceCodeUrl(self, value: str) -> None:
        """Setter: Source Code Url"""
        self._inner_dict['sourceCodeUrl'] = value
    
    
class SourceCodeUrlTypeClass(object):
    # No docs available.
    
    ML_MODEL_SOURCE_CODE = "ML_MODEL_SOURCE_CODE"
    TRAINING_PIPELINE_SOURCE_CODE = "TRAINING_PIPELINE_SOURCE_CODE"
    EVALUATION_PIPELINE_SOURCE_CODE = "EVALUATION_PIPELINE_SOURCE_CODE"
    
    
class TrainingDataClass(DictWrapper):
    """Ideally, the MLModel card would contain as much information about the training data as the evaluation data. However, there might be cases where it is not feasible to provide this level of detailed information about the training data. For example, the data may be proprietary, or require a non-disclosure agreement. In these cases, we advocate for basic details about the distributions over groups in the data, as well as any other details that could inform stakeholders on the kinds of biases the model may have encoded."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.ml.metadata.TrainingData")
    def __init__(self,
        trainingData: List["BaseDataClass"],
    ):
        super().__init__()
        
        self.trainingData = trainingData
    
    @classmethod
    def construct_with_defaults(cls) -> "TrainingDataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.trainingData = list()
    
    
    @property
    def trainingData(self) -> List["BaseDataClass"]:
        """Getter: Details on the dataset(s) used for training the MLModel"""
        return self._inner_dict.get('trainingData')  # type: ignore
    
    
    @trainingData.setter
    def trainingData(self, value: List["BaseDataClass"]) -> None:
        """Setter: Details on the dataset(s) used for training the MLModel"""
        self._inner_dict['trainingData'] = value
    
    
class MetadataChangeEventClass(DictWrapper):
    """Kafka event for proposing a metadata change for an entity. A corresponding MetadataAuditEvent is emitted when the change is accepted and committed, otherwise a FailedMetadataChangeEvent will be emitted instead."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.mxe.MetadataChangeEvent")
    def __init__(self,
        proposedSnapshot: Union["ChartSnapshotClass", "CorpGroupSnapshotClass", "CorpUserSnapshotClass", "DashboardSnapshotClass", "DataFlowSnapshotClass", "DataJobSnapshotClass", "DatasetSnapshotClass", "DataProcessSnapshotClass", "MLModelSnapshotClass", "MLFeatureSnapshotClass", "TagSnapshotClass", "GlossaryTermSnapshotClass", "GlossaryNodeSnapshotClass"],
        auditHeader: Union[None, "KafkaAuditHeaderClass"]=None,
        proposedDelta: None=None,
    ):
        super().__init__()
        
        self.auditHeader = auditHeader
        self.proposedSnapshot = proposedSnapshot
        self.proposedDelta = proposedDelta
    
    @classmethod
    def construct_with_defaults(cls) -> "MetadataChangeEventClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.auditHeader = self.RECORD_SCHEMA.field_map["auditHeader"].default
        self.proposedSnapshot = ChartSnapshotClass.construct_with_defaults()
        self.proposedDelta = self.RECORD_SCHEMA.field_map["proposedDelta"].default
    
    
    @property
    def auditHeader(self) -> Union[None, "KafkaAuditHeaderClass"]:
        """Getter: Kafka audit header. See go/kafkaauditheader for more info."""
        return self._inner_dict.get('auditHeader')  # type: ignore
    
    
    @auditHeader.setter
    def auditHeader(self, value: Union[None, "KafkaAuditHeaderClass"]) -> None:
        """Setter: Kafka audit header. See go/kafkaauditheader for more info."""
        self._inner_dict['auditHeader'] = value
    
    
    @property
    def proposedSnapshot(self) -> Union["ChartSnapshotClass", "CorpGroupSnapshotClass", "CorpUserSnapshotClass", "DashboardSnapshotClass", "DataFlowSnapshotClass", "DataJobSnapshotClass", "DatasetSnapshotClass", "DataProcessSnapshotClass", "MLModelSnapshotClass", "MLFeatureSnapshotClass", "TagSnapshotClass", "GlossaryTermSnapshotClass", "GlossaryNodeSnapshotClass"]:
        """Getter: Snapshot of the proposed metadata change. Include only the aspects affected by the change in the snapshot."""
        return self._inner_dict.get('proposedSnapshot')  # type: ignore
    
    
    @proposedSnapshot.setter
    def proposedSnapshot(self, value: Union["ChartSnapshotClass", "CorpGroupSnapshotClass", "CorpUserSnapshotClass", "DashboardSnapshotClass", "DataFlowSnapshotClass", "DataJobSnapshotClass", "DatasetSnapshotClass", "DataProcessSnapshotClass", "MLModelSnapshotClass", "MLFeatureSnapshotClass", "TagSnapshotClass", "GlossaryTermSnapshotClass", "GlossaryNodeSnapshotClass"]) -> None:
        """Setter: Snapshot of the proposed metadata change. Include only the aspects affected by the change in the snapshot."""
        self._inner_dict['proposedSnapshot'] = value
    
    
    @property
    def proposedDelta(self) -> None:
        """Getter: Delta of the proposed metadata partial update."""
        return self._inner_dict.get('proposedDelta')  # type: ignore
    
    
    @proposedDelta.setter
    def proposedDelta(self, value: None) -> None:
        """Setter: Delta of the proposed metadata partial update."""
        self._inner_dict['proposedDelta'] = value
    
    
class ArrayTypeClass(DictWrapper):
    """Array field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.ArrayType")
    def __init__(self,
        nestedType: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.nestedType = nestedType
    
    @classmethod
    def construct_with_defaults(cls) -> "ArrayTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.nestedType = self.RECORD_SCHEMA.field_map["nestedType"].default
    
    
    @property
    def nestedType(self) -> Union[None, List[str]]:
        """Getter: List of types this array holds."""
        return self._inner_dict.get('nestedType')  # type: ignore
    
    
    @nestedType.setter
    def nestedType(self, value: Union[None, List[str]]) -> None:
        """Setter: List of types this array holds."""
        self._inner_dict['nestedType'] = value
    
    
class BinaryJsonSchemaClass(DictWrapper):
    """Schema text of binary JSON schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.BinaryJsonSchema")
    def __init__(self,
        schema: str,
    ):
        super().__init__()
        
        self.schema = schema
    
    @classmethod
    def construct_with_defaults(cls) -> "BinaryJsonSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.schema = str()
    
    
    @property
    def schema(self) -> str:
        """Getter: The native schema text for binary JSON file format."""
        return self._inner_dict.get('schema')  # type: ignore
    
    
    @schema.setter
    def schema(self, value: str) -> None:
        """Setter: The native schema text for binary JSON file format."""
        self._inner_dict['schema'] = value
    
    
class BooleanTypeClass(DictWrapper):
    """Boolean field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.BooleanType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "BooleanTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class BytesTypeClass(DictWrapper):
    """Bytes field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.BytesType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "BytesTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class DatasetFieldForeignKeyClass(DictWrapper):
    """For non-urn based foregin keys."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.DatasetFieldForeignKey")
    def __init__(self,
        parentDataset: str,
        currentFieldPaths: List[str],
        parentField: str,
    ):
        super().__init__()
        
        self.parentDataset = parentDataset
        self.currentFieldPaths = currentFieldPaths
        self.parentField = parentField
    
    @classmethod
    def construct_with_defaults(cls) -> "DatasetFieldForeignKeyClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.parentDataset = str()
        self.currentFieldPaths = list()
        self.parentField = str()
    
    
    @property
    def parentDataset(self) -> str:
        """Getter: dataset that stores the resource."""
        return self._inner_dict.get('parentDataset')  # type: ignore
    
    
    @parentDataset.setter
    def parentDataset(self, value: str) -> None:
        """Setter: dataset that stores the resource."""
        self._inner_dict['parentDataset'] = value
    
    
    @property
    def currentFieldPaths(self) -> List[str]:
        """Getter: List of fields in hosting(current) SchemaMetadata that conform a foreign key. List can contain a single entry or multiple entries if several entries in hosting schema conform a foreign key in a single parent dataset."""
        return self._inner_dict.get('currentFieldPaths')  # type: ignore
    
    
    @currentFieldPaths.setter
    def currentFieldPaths(self, value: List[str]) -> None:
        """Setter: List of fields in hosting(current) SchemaMetadata that conform a foreign key. List can contain a single entry or multiple entries if several entries in hosting schema conform a foreign key in a single parent dataset."""
        self._inner_dict['currentFieldPaths'] = value
    
    
    @property
    def parentField(self) -> str:
        """Getter: SchemaField@fieldPath that uniquely identify field in parent dataset that this field references."""
        return self._inner_dict.get('parentField')  # type: ignore
    
    
    @parentField.setter
    def parentField(self, value: str) -> None:
        """Setter: SchemaField@fieldPath that uniquely identify field in parent dataset that this field references."""
        self._inner_dict['parentField'] = value
    
    
class DateTypeClass(DictWrapper):
    """Date field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.DateType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "DateTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class EditableSchemaFieldInfoClass(DictWrapper):
    """SchemaField to describe metadata related to dataset schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.EditableSchemaFieldInfo")
    def __init__(self,
        fieldPath: str,
        description: Union[None, str]=None,
        globalTags: Union[None, "GlobalTagsClass"]=None,
    ):
        super().__init__()
        
        self.fieldPath = fieldPath
        self.description = description
        self.globalTags = globalTags
    
    @classmethod
    def construct_with_defaults(cls) -> "EditableSchemaFieldInfoClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.fieldPath = str()
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.globalTags = self.RECORD_SCHEMA.field_map["globalTags"].default
    
    
    @property
    def fieldPath(self) -> str:
        """Getter: FieldPath uniquely identifying the SchemaField this metadata is associated with"""
        return self._inner_dict.get('fieldPath')  # type: ignore
    
    
    @fieldPath.setter
    def fieldPath(self, value: str) -> None:
        """Setter: FieldPath uniquely identifying the SchemaField this metadata is associated with"""
        self._inner_dict['fieldPath'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Description"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Description"""
        self._inner_dict['description'] = value
    
    
    @property
    def globalTags(self) -> Union[None, "GlobalTagsClass"]:
        """Getter: Tags associated with the field"""
        return self._inner_dict.get('globalTags')  # type: ignore
    
    
    @globalTags.setter
    def globalTags(self, value: Union[None, "GlobalTagsClass"]) -> None:
        """Setter: Tags associated with the field"""
        self._inner_dict['globalTags'] = value
    
    
class EditableSchemaMetadataClass(DictWrapper):
    """EditableSchemaMetadata stores editable changes made to schema metadata. This separates changes made from
    ingestion pipelines and edits in the UI to avoid accidental overwrites of user-provided data by ingestion pipelines."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.EditableSchemaMetadata")
    def __init__(self,
        created: "AuditStampClass",
        lastModified: "AuditStampClass",
        editableSchemaFieldInfo: List["EditableSchemaFieldInfoClass"],
        deleted: Union[None, "AuditStampClass"]=None,
    ):
        super().__init__()
        
        self.created = created
        self.lastModified = lastModified
        self.deleted = deleted
        self.editableSchemaFieldInfo = editableSchemaFieldInfo
    
    @classmethod
    def construct_with_defaults(cls) -> "EditableSchemaMetadataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.created = AuditStampClass.construct_with_defaults()
        self.lastModified = AuditStampClass.construct_with_defaults()
        self.deleted = self.RECORD_SCHEMA.field_map["deleted"].default
        self.editableSchemaFieldInfo = list()
    
    
    @property
    def created(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        return self._inner_dict.get('created')  # type: ignore
    
    
    @created.setter
    def created(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        self._inner_dict['created'] = value
    
    
    @property
    def lastModified(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        self._inner_dict['lastModified'] = value
    
    
    @property
    def deleted(self) -> Union[None, "AuditStampClass"]:
        """Getter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        return self._inner_dict.get('deleted')  # type: ignore
    
    
    @deleted.setter
    def deleted(self, value: Union[None, "AuditStampClass"]) -> None:
        """Setter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        self._inner_dict['deleted'] = value
    
    
    @property
    def editableSchemaFieldInfo(self) -> List["EditableSchemaFieldInfoClass"]:
        """Getter: Client provided a list of fields from document schema."""
        return self._inner_dict.get('editableSchemaFieldInfo')  # type: ignore
    
    
    @editableSchemaFieldInfo.setter
    def editableSchemaFieldInfo(self, value: List["EditableSchemaFieldInfoClass"]) -> None:
        """Setter: Client provided a list of fields from document schema."""
        self._inner_dict['editableSchemaFieldInfo'] = value
    
    
class EnumTypeClass(DictWrapper):
    """Enum field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.EnumType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "EnumTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class EspressoSchemaClass(DictWrapper):
    """Schema text of an espresso table schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.EspressoSchema")
    def __init__(self,
        documentSchema: str,
        tableSchema: str,
    ):
        super().__init__()
        
        self.documentSchema = documentSchema
        self.tableSchema = tableSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "EspressoSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.documentSchema = str()
        self.tableSchema = str()
    
    
    @property
    def documentSchema(self) -> str:
        """Getter: The native espresso document schema."""
        return self._inner_dict.get('documentSchema')  # type: ignore
    
    
    @documentSchema.setter
    def documentSchema(self, value: str) -> None:
        """Setter: The native espresso document schema."""
        self._inner_dict['documentSchema'] = value
    
    
    @property
    def tableSchema(self) -> str:
        """Getter: The espresso table schema definition."""
        return self._inner_dict.get('tableSchema')  # type: ignore
    
    
    @tableSchema.setter
    def tableSchema(self, value: str) -> None:
        """Setter: The espresso table schema definition."""
        self._inner_dict['tableSchema'] = value
    
    
class FixedTypeClass(DictWrapper):
    """Fixed field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.FixedType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "FixedTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class ForeignKeySpecClass(DictWrapper):
    """Description of a foreign key in a schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.ForeignKeySpec")
    def __init__(self,
        foreignKey: Union["DatasetFieldForeignKeyClass", "UrnForeignKeyClass"],
    ):
        super().__init__()
        
        self.foreignKey = foreignKey
    
    @classmethod
    def construct_with_defaults(cls) -> "ForeignKeySpecClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.foreignKey = DatasetFieldForeignKeyClass.construct_with_defaults()
    
    
    @property
    def foreignKey(self) -> Union["DatasetFieldForeignKeyClass", "UrnForeignKeyClass"]:
        """Getter: Foreign key definition in metadata schema."""
        return self._inner_dict.get('foreignKey')  # type: ignore
    
    
    @foreignKey.setter
    def foreignKey(self, value: Union["DatasetFieldForeignKeyClass", "UrnForeignKeyClass"]) -> None:
        """Setter: Foreign key definition in metadata schema."""
        self._inner_dict['foreignKey'] = value
    
    
class KafkaSchemaClass(DictWrapper):
    """Schema holder for kafka schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.KafkaSchema")
    def __init__(self,
        documentSchema: str,
    ):
        super().__init__()
        
        self.documentSchema = documentSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "KafkaSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.documentSchema = str()
    
    
    @property
    def documentSchema(self) -> str:
        """Getter: The native kafka document schema. This is a human readable avro document schema."""
        return self._inner_dict.get('documentSchema')  # type: ignore
    
    
    @documentSchema.setter
    def documentSchema(self, value: str) -> None:
        """Setter: The native kafka document schema. This is a human readable avro document schema."""
        self._inner_dict['documentSchema'] = value
    
    
class KeyValueSchemaClass(DictWrapper):
    """Schema text of a key-value store schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.KeyValueSchema")
    def __init__(self,
        keySchema: str,
        valueSchema: str,
    ):
        super().__init__()
        
        self.keySchema = keySchema
        self.valueSchema = valueSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "KeyValueSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.keySchema = str()
        self.valueSchema = str()
    
    
    @property
    def keySchema(self) -> str:
        """Getter: The raw schema for the key in the key-value store."""
        return self._inner_dict.get('keySchema')  # type: ignore
    
    
    @keySchema.setter
    def keySchema(self, value: str) -> None:
        """Setter: The raw schema for the key in the key-value store."""
        self._inner_dict['keySchema'] = value
    
    
    @property
    def valueSchema(self) -> str:
        """Getter: The raw schema for the value in the key-value store."""
        return self._inner_dict.get('valueSchema')  # type: ignore
    
    
    @valueSchema.setter
    def valueSchema(self, value: str) -> None:
        """Setter: The raw schema for the value in the key-value store."""
        self._inner_dict['valueSchema'] = value
    
    
class MapTypeClass(DictWrapper):
    """Map field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.MapType")
    def __init__(self,
        keyType: Union[None, str]=None,
        valueType: Union[None, str]=None,
    ):
        super().__init__()
        
        self.keyType = keyType
        self.valueType = valueType
    
    @classmethod
    def construct_with_defaults(cls) -> "MapTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.keyType = self.RECORD_SCHEMA.field_map["keyType"].default
        self.valueType = self.RECORD_SCHEMA.field_map["valueType"].default
    
    
    @property
    def keyType(self) -> Union[None, str]:
        """Getter: Key type in a map"""
        return self._inner_dict.get('keyType')  # type: ignore
    
    
    @keyType.setter
    def keyType(self, value: Union[None, str]) -> None:
        """Setter: Key type in a map"""
        self._inner_dict['keyType'] = value
    
    
    @property
    def valueType(self) -> Union[None, str]:
        """Getter: Type of the value in a map"""
        return self._inner_dict.get('valueType')  # type: ignore
    
    
    @valueType.setter
    def valueType(self, value: Union[None, str]) -> None:
        """Setter: Type of the value in a map"""
        self._inner_dict['valueType'] = value
    
    
class MySqlDDLClass(DictWrapper):
    """Schema holder for MySql data definition language that describes an MySql table."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.MySqlDDL")
    def __init__(self,
        tableSchema: str,
    ):
        super().__init__()
        
        self.tableSchema = tableSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "MySqlDDLClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.tableSchema = str()
    
    
    @property
    def tableSchema(self) -> str:
        """Getter: The native schema in the dataset's platform. This is a human readable (json blob) table schema."""
        return self._inner_dict.get('tableSchema')  # type: ignore
    
    
    @tableSchema.setter
    def tableSchema(self, value: str) -> None:
        """Setter: The native schema in the dataset's platform. This is a human readable (json blob) table schema."""
        self._inner_dict['tableSchema'] = value
    
    
class NullTypeClass(DictWrapper):
    """Null field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.NullType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "NullTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class NumberTypeClass(DictWrapper):
    """Number data type: long, integer, short, etc.."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.NumberType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "NumberTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class OracleDDLClass(DictWrapper):
    """Schema holder for oracle data definition language that describes an oracle table."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.OracleDDL")
    def __init__(self,
        tableSchema: str,
    ):
        super().__init__()
        
        self.tableSchema = tableSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "OracleDDLClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.tableSchema = str()
    
    
    @property
    def tableSchema(self) -> str:
        """Getter: The native schema in the dataset's platform. This is a human readable (json blob) table schema."""
        return self._inner_dict.get('tableSchema')  # type: ignore
    
    
    @tableSchema.setter
    def tableSchema(self, value: str) -> None:
        """Setter: The native schema in the dataset's platform. This is a human readable (json blob) table schema."""
        self._inner_dict['tableSchema'] = value
    
    
class OrcSchemaClass(DictWrapper):
    """Schema text of an ORC schema."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.OrcSchema")
    def __init__(self,
        schema: str,
    ):
        super().__init__()
        
        self.schema = schema
    
    @classmethod
    def construct_with_defaults(cls) -> "OrcSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.schema = str()
    
    
    @property
    def schema(self) -> str:
        """Getter: The native schema for ORC file format."""
        return self._inner_dict.get('schema')  # type: ignore
    
    
    @schema.setter
    def schema(self, value: str) -> None:
        """Setter: The native schema for ORC file format."""
        self._inner_dict['schema'] = value
    
    
class OtherSchemaClass(DictWrapper):
    """Schema holder for undefined schema types."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.OtherSchema")
    def __init__(self,
        rawSchema: str,
    ):
        super().__init__()
        
        self.rawSchema = rawSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "OtherSchemaClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.rawSchema = str()
    
    
    @property
    def rawSchema(self) -> str:
        """Getter: The native schema in the dataset's platform."""
        return self._inner_dict.get('rawSchema')  # type: ignore
    
    
    @rawSchema.setter
    def rawSchema(self, value: str) -> None:
        """Setter: The native schema in the dataset's platform."""
        self._inner_dict['rawSchema'] = value
    
    
class PrestoDDLClass(DictWrapper):
    """Schema holder for presto data definition language that describes a presto view."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.PrestoDDL")
    def __init__(self,
        rawSchema: str,
    ):
        super().__init__()
        
        self.rawSchema = rawSchema
    
    @classmethod
    def construct_with_defaults(cls) -> "PrestoDDLClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.rawSchema = str()
    
    
    @property
    def rawSchema(self) -> str:
        """Getter: The raw schema in the dataset's platform. This includes the DDL and the columns extracted from DDL."""
        return self._inner_dict.get('rawSchema')  # type: ignore
    
    
    @rawSchema.setter
    def rawSchema(self, value: str) -> None:
        """Setter: The raw schema in the dataset's platform. This includes the DDL and the columns extracted from DDL."""
        self._inner_dict['rawSchema'] = value
    
    
class RecordTypeClass(DictWrapper):
    """Record field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.RecordType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "RecordTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class SchemaFieldClass(DictWrapper):
    """SchemaField to describe metadata related to dataset schema. Schema normalization rules: http://go/tms-schema"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.SchemaField")
    def __init__(self,
        fieldPath: str,
        type: "SchemaFieldDataTypeClass",
        nativeDataType: str,
        jsonPath: Union[None, str]=None,
        nullable: Optional[bool]=None,
        description: Union[None, str]=None,
        recursive: Optional[bool]=None,
        globalTags: Union[None, "GlobalTagsClass"]=None,
        glossaryTerms: Union[None, "GlossaryTermsClass"]=None,
    ):
        super().__init__()
        
        self.fieldPath = fieldPath
        self.jsonPath = jsonPath
        if nullable is None:
            self.nullable = False
        else:
            self.nullable = nullable
        self.description = description
        self.type = type
        self.nativeDataType = nativeDataType
        if recursive is None:
            self.recursive = False
        else:
            self.recursive = recursive
        self.globalTags = globalTags
        self.glossaryTerms = glossaryTerms
    
    @classmethod
    def construct_with_defaults(cls) -> "SchemaFieldClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.fieldPath = str()
        self.jsonPath = self.RECORD_SCHEMA.field_map["jsonPath"].default
        self.nullable = self.RECORD_SCHEMA.field_map["nullable"].default
        self.description = self.RECORD_SCHEMA.field_map["description"].default
        self.type = SchemaFieldDataTypeClass.construct_with_defaults()
        self.nativeDataType = str()
        self.recursive = self.RECORD_SCHEMA.field_map["recursive"].default
        self.globalTags = self.RECORD_SCHEMA.field_map["globalTags"].default
        self.glossaryTerms = self.RECORD_SCHEMA.field_map["glossaryTerms"].default
    
    
    @property
    def fieldPath(self) -> str:
        """Getter: Flattened name of the field. Field is computed from jsonPath field. For data translation rules refer to wiki page above."""
        return self._inner_dict.get('fieldPath')  # type: ignore
    
    
    @fieldPath.setter
    def fieldPath(self, value: str) -> None:
        """Setter: Flattened name of the field. Field is computed from jsonPath field. For data translation rules refer to wiki page above."""
        self._inner_dict['fieldPath'] = value
    
    
    @property
    def jsonPath(self) -> Union[None, str]:
        """Getter: Flattened name of a field in JSON Path notation."""
        return self._inner_dict.get('jsonPath')  # type: ignore
    
    
    @jsonPath.setter
    def jsonPath(self, value: Union[None, str]) -> None:
        """Setter: Flattened name of a field in JSON Path notation."""
        self._inner_dict['jsonPath'] = value
    
    
    @property
    def nullable(self) -> bool:
        """Getter: Indicates if this field is optional or nullable"""
        return self._inner_dict.get('nullable')  # type: ignore
    
    
    @nullable.setter
    def nullable(self, value: bool) -> None:
        """Setter: Indicates if this field is optional or nullable"""
        self._inner_dict['nullable'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Description"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Description"""
        self._inner_dict['description'] = value
    
    
    @property
    def type(self) -> "SchemaFieldDataTypeClass":
        """Getter: Platform independent field type of the field."""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: "SchemaFieldDataTypeClass") -> None:
        """Setter: Platform independent field type of the field."""
        self._inner_dict['type'] = value
    
    
    @property
    def nativeDataType(self) -> str:
        """Getter: The native type of the field in the dataset's platform as declared by platform schema."""
        return self._inner_dict.get('nativeDataType')  # type: ignore
    
    
    @nativeDataType.setter
    def nativeDataType(self, value: str) -> None:
        """Setter: The native type of the field in the dataset's platform as declared by platform schema."""
        self._inner_dict['nativeDataType'] = value
    
    
    @property
    def recursive(self) -> bool:
        """Getter: There are use cases when a field in type B references type A. A field in A references field of type B. In such cases, we will mark the first field as recursive."""
        return self._inner_dict.get('recursive')  # type: ignore
    
    
    @recursive.setter
    def recursive(self, value: bool) -> None:
        """Setter: There are use cases when a field in type B references type A. A field in A references field of type B. In such cases, we will mark the first field as recursive."""
        self._inner_dict['recursive'] = value
    
    
    @property
    def globalTags(self) -> Union[None, "GlobalTagsClass"]:
        """Getter: Tags associated with the field"""
        return self._inner_dict.get('globalTags')  # type: ignore
    
    
    @globalTags.setter
    def globalTags(self, value: Union[None, "GlobalTagsClass"]) -> None:
        """Setter: Tags associated with the field"""
        self._inner_dict['globalTags'] = value
    
    
    @property
    def glossaryTerms(self) -> Union[None, "GlossaryTermsClass"]:
        """Getter: Glossary terms associated with the field"""
        return self._inner_dict.get('glossaryTerms')  # type: ignore
    
    
    @glossaryTerms.setter
    def glossaryTerms(self, value: Union[None, "GlossaryTermsClass"]) -> None:
        """Setter: Glossary terms associated with the field"""
        self._inner_dict['glossaryTerms'] = value
    
    
class SchemaFieldDataTypeClass(DictWrapper):
    """Schema field data types"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.SchemaFieldDataType")
    def __init__(self,
        type: Union["BooleanTypeClass", "FixedTypeClass", "StringTypeClass", "BytesTypeClass", "NumberTypeClass", "DateTypeClass", "TimeTypeClass", "EnumTypeClass", "NullTypeClass", "MapTypeClass", "ArrayTypeClass", "UnionTypeClass", "RecordTypeClass"],
    ):
        super().__init__()
        
        self.type = type
    
    @classmethod
    def construct_with_defaults(cls) -> "SchemaFieldDataTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.type = BooleanTypeClass.construct_with_defaults()
    
    
    @property
    def type(self) -> Union["BooleanTypeClass", "FixedTypeClass", "StringTypeClass", "BytesTypeClass", "NumberTypeClass", "DateTypeClass", "TimeTypeClass", "EnumTypeClass", "NullTypeClass", "MapTypeClass", "ArrayTypeClass", "UnionTypeClass", "RecordTypeClass"]:
        """Getter: Data platform specific types"""
        return self._inner_dict.get('type')  # type: ignore
    
    
    @type.setter
    def type(self, value: Union["BooleanTypeClass", "FixedTypeClass", "StringTypeClass", "BytesTypeClass", "NumberTypeClass", "DateTypeClass", "TimeTypeClass", "EnumTypeClass", "NullTypeClass", "MapTypeClass", "ArrayTypeClass", "UnionTypeClass", "RecordTypeClass"]) -> None:
        """Setter: Data platform specific types"""
        self._inner_dict['type'] = value
    
    
class SchemaMetadataClass(DictWrapper):
    """SchemaMetadata to describe metadata related to store schema"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.SchemaMetadata")
    def __init__(self,
        schemaName: str,
        platform: str,
        version: int,
        created: "AuditStampClass",
        lastModified: "AuditStampClass",
        hash: str,
        platformSchema: Union["EspressoSchemaClass", "OracleDDLClass", "MySqlDDLClass", "PrestoDDLClass", "KafkaSchemaClass", "BinaryJsonSchemaClass", "OrcSchemaClass", "SchemalessClass", "KeyValueSchemaClass", "OtherSchemaClass"],
        fields: List["SchemaFieldClass"],
        deleted: Union[None, "AuditStampClass"]=None,
        dataset: Union[None, str]=None,
        cluster: Union[None, str]=None,
        primaryKeys: Union[None, List[str]]=None,
        foreignKeysSpecs: Union[None, Dict[str, "ForeignKeySpecClass"]]=None,
    ):
        super().__init__()
        
        self.schemaName = schemaName
        self.platform = platform
        self.version = version
        self.created = created
        self.lastModified = lastModified
        self.deleted = deleted
        self.dataset = dataset
        self.cluster = cluster
        self.hash = hash
        self.platformSchema = platformSchema
        self.fields = fields
        self.primaryKeys = primaryKeys
        self.foreignKeysSpecs = foreignKeysSpecs
    
    @classmethod
    def construct_with_defaults(cls) -> "SchemaMetadataClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.schemaName = str()
        self.platform = str()
        self.version = int()
        self.created = AuditStampClass.construct_with_defaults()
        self.lastModified = AuditStampClass.construct_with_defaults()
        self.deleted = self.RECORD_SCHEMA.field_map["deleted"].default
        self.dataset = self.RECORD_SCHEMA.field_map["dataset"].default
        self.cluster = self.RECORD_SCHEMA.field_map["cluster"].default
        self.hash = str()
        self.platformSchema = EspressoSchemaClass.construct_with_defaults()
        self.fields = list()
        self.primaryKeys = self.RECORD_SCHEMA.field_map["primaryKeys"].default
        self.foreignKeysSpecs = self.RECORD_SCHEMA.field_map["foreignKeysSpecs"].default
    
    
    @property
    def schemaName(self) -> str:
        """Getter: Schema name e.g. PageViewEvent, identity.Profile, ams.account_management_tracking"""
        return self._inner_dict.get('schemaName')  # type: ignore
    
    
    @schemaName.setter
    def schemaName(self, value: str) -> None:
        """Setter: Schema name e.g. PageViewEvent, identity.Profile, ams.account_management_tracking"""
        self._inner_dict['schemaName'] = value
    
    
    @property
    def platform(self) -> str:
        """Getter: Standardized platform urn where schema is defined. The data platform Urn (urn:li:platform:{platform_name})"""
        return self._inner_dict.get('platform')  # type: ignore
    
    
    @platform.setter
    def platform(self, value: str) -> None:
        """Setter: Standardized platform urn where schema is defined. The data platform Urn (urn:li:platform:{platform_name})"""
        self._inner_dict['platform'] = value
    
    
    @property
    def version(self) -> int:
        """Getter: Every change to SchemaMetadata in the resource results in a new version. Version is server assigned. This version is differ from platform native schema version."""
        return self._inner_dict.get('version')  # type: ignore
    
    
    @version.setter
    def version(self, value: int) -> None:
        """Setter: Every change to SchemaMetadata in the resource results in a new version. Version is server assigned. This version is differ from platform native schema version."""
        self._inner_dict['version'] = value
    
    
    @property
    def created(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        return self._inner_dict.get('created')  # type: ignore
    
    
    @created.setter
    def created(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the creation of this resource/association/sub-resource"""
        self._inner_dict['created'] = value
    
    
    @property
    def lastModified(self) -> "AuditStampClass":
        """Getter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        return self._inner_dict.get('lastModified')  # type: ignore
    
    
    @lastModified.setter
    def lastModified(self, value: "AuditStampClass") -> None:
        """Setter: An AuditStamp corresponding to the last modification of this resource/association/sub-resource. If no modification has happened since creation, lastModified should be the same as created"""
        self._inner_dict['lastModified'] = value
    
    
    @property
    def deleted(self) -> Union[None, "AuditStampClass"]:
        """Getter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        return self._inner_dict.get('deleted')  # type: ignore
    
    
    @deleted.setter
    def deleted(self, value: Union[None, "AuditStampClass"]) -> None:
        """Setter: An AuditStamp corresponding to the deletion of this resource/association/sub-resource. Logically, deleted MUST have a later timestamp than creation. It may or may not have the same time as lastModified depending upon the resource/association/sub-resource semantics."""
        self._inner_dict['deleted'] = value
    
    
    @property
    def dataset(self) -> Union[None, str]:
        """Getter: Dataset this schema metadata is associated with."""
        return self._inner_dict.get('dataset')  # type: ignore
    
    
    @dataset.setter
    def dataset(self, value: Union[None, str]) -> None:
        """Setter: Dataset this schema metadata is associated with."""
        self._inner_dict['dataset'] = value
    
    
    @property
    def cluster(self) -> Union[None, str]:
        """Getter: The cluster this schema metadata resides from"""
        return self._inner_dict.get('cluster')  # type: ignore
    
    
    @cluster.setter
    def cluster(self, value: Union[None, str]) -> None:
        """Setter: The cluster this schema metadata resides from"""
        self._inner_dict['cluster'] = value
    
    
    @property
    def hash(self) -> str:
        """Getter: the SHA1 hash of the schema content"""
        return self._inner_dict.get('hash')  # type: ignore
    
    
    @hash.setter
    def hash(self, value: str) -> None:
        """Setter: the SHA1 hash of the schema content"""
        self._inner_dict['hash'] = value
    
    
    @property
    def platformSchema(self) -> Union["EspressoSchemaClass", "OracleDDLClass", "MySqlDDLClass", "PrestoDDLClass", "KafkaSchemaClass", "BinaryJsonSchemaClass", "OrcSchemaClass", "SchemalessClass", "KeyValueSchemaClass", "OtherSchemaClass"]:
        """Getter: The native schema in the dataset's platform."""
        return self._inner_dict.get('platformSchema')  # type: ignore
    
    
    @platformSchema.setter
    def platformSchema(self, value: Union["EspressoSchemaClass", "OracleDDLClass", "MySqlDDLClass", "PrestoDDLClass", "KafkaSchemaClass", "BinaryJsonSchemaClass", "OrcSchemaClass", "SchemalessClass", "KeyValueSchemaClass", "OtherSchemaClass"]) -> None:
        """Setter: The native schema in the dataset's platform."""
        self._inner_dict['platformSchema'] = value
    
    
    @property
    def fields(self) -> List["SchemaFieldClass"]:
        """Getter: Client provided a list of fields from document schema."""
        return self._inner_dict.get('fields')  # type: ignore
    
    
    @fields.setter
    def fields(self, value: List["SchemaFieldClass"]) -> None:
        """Setter: Client provided a list of fields from document schema."""
        self._inner_dict['fields'] = value
    
    
    @property
    def primaryKeys(self) -> Union[None, List[str]]:
        """Getter: Client provided list of fields that define primary keys to access record. Field order defines hierarchical espresso keys. Empty lists indicates absence of primary key access patter. Value is a SchemaField@fieldPath."""
        return self._inner_dict.get('primaryKeys')  # type: ignore
    
    
    @primaryKeys.setter
    def primaryKeys(self, value: Union[None, List[str]]) -> None:
        """Setter: Client provided list of fields that define primary keys to access record. Field order defines hierarchical espresso keys. Empty lists indicates absence of primary key access patter. Value is a SchemaField@fieldPath."""
        self._inner_dict['primaryKeys'] = value
    
    
    @property
    def foreignKeysSpecs(self) -> Union[None, Dict[str, "ForeignKeySpecClass"]]:
        """Getter: Map captures all the references schema makes to external datasets. Map key is ForeignKeySpecName typeref."""
        return self._inner_dict.get('foreignKeysSpecs')  # type: ignore
    
    
    @foreignKeysSpecs.setter
    def foreignKeysSpecs(self, value: Union[None, Dict[str, "ForeignKeySpecClass"]]) -> None:
        """Setter: Map captures all the references schema makes to external datasets. Map key is ForeignKeySpecName typeref."""
        self._inner_dict['foreignKeysSpecs'] = value
    
    
class SchemalessClass(DictWrapper):
    """The dataset has no specific schema associated with it"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.Schemaless")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "SchemalessClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class StringTypeClass(DictWrapper):
    """String field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.StringType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "StringTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class TimeTypeClass(DictWrapper):
    """Time field type. This should also be used for datetimes."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.TimeType")
    def __init__(self,
    ):
        super().__init__()
        
    
    @classmethod
    def construct_with_defaults(cls) -> "TimeTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        pass
    
    
class UnionTypeClass(DictWrapper):
    """Union field type."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.UnionType")
    def __init__(self,
        nestedTypes: Union[None, List[str]]=None,
    ):
        super().__init__()
        
        self.nestedTypes = nestedTypes
    
    @classmethod
    def construct_with_defaults(cls) -> "UnionTypeClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.nestedTypes = self.RECORD_SCHEMA.field_map["nestedTypes"].default
    
    
    @property
    def nestedTypes(self) -> Union[None, List[str]]:
        """Getter: List of types in union type."""
        return self._inner_dict.get('nestedTypes')  # type: ignore
    
    
    @nestedTypes.setter
    def nestedTypes(self, value: Union[None, List[str]]) -> None:
        """Setter: List of types in union type."""
        self._inner_dict['nestedTypes'] = value
    
    
class UrnForeignKeyClass(DictWrapper):
    """If SchemaMetadata fields make any external references and references are of type com.linkedin.pegasus2avro.common.Urn or any children, this models can be used to mark it."""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.schema.UrnForeignKey")
    def __init__(self,
        currentFieldPath: str,
    ):
        super().__init__()
        
        self.currentFieldPath = currentFieldPath
    
    @classmethod
    def construct_with_defaults(cls) -> "UrnForeignKeyClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.currentFieldPath = str()
    
    
    @property
    def currentFieldPath(self) -> str:
        """Getter: Field in hosting(current) SchemaMetadata."""
        return self._inner_dict.get('currentFieldPath')  # type: ignore
    
    
    @currentFieldPath.setter
    def currentFieldPath(self, value: str) -> None:
        """Setter: Field in hosting(current) SchemaMetadata."""
        self._inner_dict['currentFieldPath'] = value
    
    
class TagPropertiesClass(DictWrapper):
    """Properties associated with a Tag"""
    
    RECORD_SCHEMA = get_schema_type("com.linkedin.pegasus2avro.tag.TagProperties")
    def __init__(self,
        name: str,
        description: Union[None, str]=None,
    ):
        super().__init__()
        
        self.name = name
        self.description = description
    
    @classmethod
    def construct_with_defaults(cls) -> "TagPropertiesClass":
        self = cls.construct({})
        self._restore_defaults()
        
        return self
    
    def _restore_defaults(self) -> None:
        self.name = str()
        self.description = self.RECORD_SCHEMA.field_map["description"].default
    
    
    @property
    def name(self) -> str:
        """Getter: Name of the tag"""
        return self._inner_dict.get('name')  # type: ignore
    
    
    @name.setter
    def name(self, value: str) -> None:
        """Setter: Name of the tag"""
        self._inner_dict['name'] = value
    
    
    @property
    def description(self) -> Union[None, str]:
        """Getter: Documentation of the tag"""
        return self._inner_dict.get('description')  # type: ignore
    
    
    @description.setter
    def description(self, value: Union[None, str]) -> None:
        """Setter: Documentation of the tag"""
        self._inner_dict['description'] = value
    
    
__SCHEMA_TYPES = {
    'com.linkedin.events.KafkaAuditHeader': KafkaAuditHeaderClass,
    'com.linkedin.pegasus2avro.chart.ChartInfo': ChartInfoClass,
    'com.linkedin.pegasus2avro.chart.ChartQuery': ChartQueryClass,
    'com.linkedin.pegasus2avro.chart.ChartQueryType': ChartQueryTypeClass,
    'com.linkedin.pegasus2avro.chart.ChartType': ChartTypeClass,
    'com.linkedin.pegasus2avro.common.AccessLevel': AccessLevelClass,
    'com.linkedin.pegasus2avro.common.AuditStamp': AuditStampClass,
    'com.linkedin.pegasus2avro.common.ChangeAuditStamps': ChangeAuditStampsClass,
    'com.linkedin.pegasus2avro.common.Cost': CostClass,
    'com.linkedin.pegasus2avro.common.CostCost': CostCostClass,
    'com.linkedin.pegasus2avro.common.CostCostDiscriminator': CostCostDiscriminatorClass,
    'com.linkedin.pegasus2avro.common.CostType': CostTypeClass,
    'com.linkedin.pegasus2avro.common.Deprecation': DeprecationClass,
    'com.linkedin.pegasus2avro.common.GlobalTags': GlobalTagsClass,
    'com.linkedin.pegasus2avro.common.GlossaryTermAssociation': GlossaryTermAssociationClass,
    'com.linkedin.pegasus2avro.common.GlossaryTerms': GlossaryTermsClass,
    'com.linkedin.pegasus2avro.common.InstitutionalMemory': InstitutionalMemoryClass,
    'com.linkedin.pegasus2avro.common.InstitutionalMemoryMetadata': InstitutionalMemoryMetadataClass,
    'com.linkedin.pegasus2avro.common.MLFeatureDataType': MLFeatureDataTypeClass,
    'com.linkedin.pegasus2avro.common.Owner': OwnerClass,
    'com.linkedin.pegasus2avro.common.Ownership': OwnershipClass,
    'com.linkedin.pegasus2avro.common.OwnershipSource': OwnershipSourceClass,
    'com.linkedin.pegasus2avro.common.OwnershipSourceType': OwnershipSourceTypeClass,
    'com.linkedin.pegasus2avro.common.OwnershipType': OwnershipTypeClass,
    'com.linkedin.pegasus2avro.common.Status': StatusClass,
    'com.linkedin.pegasus2avro.common.TagAssociation': TagAssociationClass,
    'com.linkedin.pegasus2avro.common.VersionTag': VersionTagClass,
    'com.linkedin.pegasus2avro.common.fieldtransformer.TransformationType': TransformationTypeClass,
    'com.linkedin.pegasus2avro.common.fieldtransformer.UDFTransformer': UDFTransformerClass,
    'com.linkedin.pegasus2avro.dashboard.DashboardInfo': DashboardInfoClass,
    'com.linkedin.pegasus2avro.datajob.DataFlowInfo': DataFlowInfoClass,
    'com.linkedin.pegasus2avro.datajob.DataJobInfo': DataJobInfoClass,
    'com.linkedin.pegasus2avro.datajob.DataJobInputOutput': DataJobInputOutputClass,
    'com.linkedin.pegasus2avro.datajob.azkaban.AzkabanJobType': AzkabanJobTypeClass,
    'com.linkedin.pegasus2avro.dataprocess.DataProcessInfo': DataProcessInfoClass,
    'com.linkedin.pegasus2avro.dataset.DatasetDeprecation': DatasetDeprecationClass,
    'com.linkedin.pegasus2avro.dataset.DatasetFieldMapping': DatasetFieldMappingClass,
    'com.linkedin.pegasus2avro.dataset.DatasetLineageType': DatasetLineageTypeClass,
    'com.linkedin.pegasus2avro.dataset.DatasetProperties': DatasetPropertiesClass,
    'com.linkedin.pegasus2avro.dataset.DatasetUpstreamLineage': DatasetUpstreamLineageClass,
    'com.linkedin.pegasus2avro.dataset.Upstream': UpstreamClass,
    'com.linkedin.pegasus2avro.dataset.UpstreamLineage': UpstreamLineageClass,
    'com.linkedin.pegasus2avro.glossary.GlossaryNodeInfo': GlossaryNodeInfoClass,
    'com.linkedin.pegasus2avro.glossary.GlossaryTermInfo': GlossaryTermInfoClass,
    'com.linkedin.pegasus2avro.identity.CorpGroupInfo': CorpGroupInfoClass,
    'com.linkedin.pegasus2avro.identity.CorpUserEditableInfo': CorpUserEditableInfoClass,
    'com.linkedin.pegasus2avro.identity.CorpUserInfo': CorpUserInfoClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.ChartSnapshot': ChartSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.CorpGroupSnapshot': CorpGroupSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.CorpUserSnapshot': CorpUserSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.DashboardSnapshot': DashboardSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.DataFlowSnapshot': DataFlowSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.DataJobSnapshot': DataJobSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.DataProcessSnapshot': DataProcessSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.DatasetSnapshot': DatasetSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.GlossaryNodeSnapshot': GlossaryNodeSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.GlossaryTermSnapshot': GlossaryTermSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.MLFeatureSnapshot': MLFeatureSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.MLModelSnapshot': MLModelSnapshotClass,
    'com.linkedin.pegasus2avro.metadata.snapshot.TagSnapshot': TagSnapshotClass,
    'com.linkedin.pegasus2avro.ml.metadata.BaseData': BaseDataClass,
    'com.linkedin.pegasus2avro.ml.metadata.CaveatDetails': CaveatDetailsClass,
    'com.linkedin.pegasus2avro.ml.metadata.CaveatsAndRecommendations': CaveatsAndRecommendationsClass,
    'com.linkedin.pegasus2avro.ml.metadata.EthicalConsiderations': EthicalConsiderationsClass,
    'com.linkedin.pegasus2avro.ml.metadata.EvaluationData': EvaluationDataClass,
    'com.linkedin.pegasus2avro.ml.metadata.IntendedUse': IntendedUseClass,
    'com.linkedin.pegasus2avro.ml.metadata.IntendedUserType': IntendedUserTypeClass,
    'com.linkedin.pegasus2avro.ml.metadata.MLFeatureProperties': MLFeaturePropertiesClass,
    'com.linkedin.pegasus2avro.ml.metadata.MLModelFactorPrompts': MLModelFactorPromptsClass,
    'com.linkedin.pegasus2avro.ml.metadata.MLModelFactors': MLModelFactorsClass,
    'com.linkedin.pegasus2avro.ml.metadata.MLModelProperties': MLModelPropertiesClass,
    'com.linkedin.pegasus2avro.ml.metadata.Metrics': MetricsClass,
    'com.linkedin.pegasus2avro.ml.metadata.QuantitativeAnalyses': QuantitativeAnalysesClass,
    'com.linkedin.pegasus2avro.ml.metadata.SourceCode': SourceCodeClass,
    'com.linkedin.pegasus2avro.ml.metadata.SourceCodeUrl': SourceCodeUrlClass,
    'com.linkedin.pegasus2avro.ml.metadata.SourceCodeUrlType': SourceCodeUrlTypeClass,
    'com.linkedin.pegasus2avro.ml.metadata.TrainingData': TrainingDataClass,
    'com.linkedin.pegasus2avro.mxe.MetadataChangeEvent': MetadataChangeEventClass,
    'com.linkedin.pegasus2avro.schema.ArrayType': ArrayTypeClass,
    'com.linkedin.pegasus2avro.schema.BinaryJsonSchema': BinaryJsonSchemaClass,
    'com.linkedin.pegasus2avro.schema.BooleanType': BooleanTypeClass,
    'com.linkedin.pegasus2avro.schema.BytesType': BytesTypeClass,
    'com.linkedin.pegasus2avro.schema.DatasetFieldForeignKey': DatasetFieldForeignKeyClass,
    'com.linkedin.pegasus2avro.schema.DateType': DateTypeClass,
    'com.linkedin.pegasus2avro.schema.EditableSchemaFieldInfo': EditableSchemaFieldInfoClass,
    'com.linkedin.pegasus2avro.schema.EditableSchemaMetadata': EditableSchemaMetadataClass,
    'com.linkedin.pegasus2avro.schema.EnumType': EnumTypeClass,
    'com.linkedin.pegasus2avro.schema.EspressoSchema': EspressoSchemaClass,
    'com.linkedin.pegasus2avro.schema.FixedType': FixedTypeClass,
    'com.linkedin.pegasus2avro.schema.ForeignKeySpec': ForeignKeySpecClass,
    'com.linkedin.pegasus2avro.schema.KafkaSchema': KafkaSchemaClass,
    'com.linkedin.pegasus2avro.schema.KeyValueSchema': KeyValueSchemaClass,
    'com.linkedin.pegasus2avro.schema.MapType': MapTypeClass,
    'com.linkedin.pegasus2avro.schema.MySqlDDL': MySqlDDLClass,
    'com.linkedin.pegasus2avro.schema.NullType': NullTypeClass,
    'com.linkedin.pegasus2avro.schema.NumberType': NumberTypeClass,
    'com.linkedin.pegasus2avro.schema.OracleDDL': OracleDDLClass,
    'com.linkedin.pegasus2avro.schema.OrcSchema': OrcSchemaClass,
    'com.linkedin.pegasus2avro.schema.OtherSchema': OtherSchemaClass,
    'com.linkedin.pegasus2avro.schema.PrestoDDL': PrestoDDLClass,
    'com.linkedin.pegasus2avro.schema.RecordType': RecordTypeClass,
    'com.linkedin.pegasus2avro.schema.SchemaField': SchemaFieldClass,
    'com.linkedin.pegasus2avro.schema.SchemaFieldDataType': SchemaFieldDataTypeClass,
    'com.linkedin.pegasus2avro.schema.SchemaMetadata': SchemaMetadataClass,
    'com.linkedin.pegasus2avro.schema.Schemaless': SchemalessClass,
    'com.linkedin.pegasus2avro.schema.StringType': StringTypeClass,
    'com.linkedin.pegasus2avro.schema.TimeType': TimeTypeClass,
    'com.linkedin.pegasus2avro.schema.UnionType': UnionTypeClass,
    'com.linkedin.pegasus2avro.schema.UrnForeignKey': UrnForeignKeyClass,
    'com.linkedin.pegasus2avro.tag.TagProperties': TagPropertiesClass,
    'KafkaAuditHeader': KafkaAuditHeaderClass,
    'ChartInfo': ChartInfoClass,
    'ChartQuery': ChartQueryClass,
    'ChartQueryType': ChartQueryTypeClass,
    'ChartType': ChartTypeClass,
    'AccessLevel': AccessLevelClass,
    'AuditStamp': AuditStampClass,
    'ChangeAuditStamps': ChangeAuditStampsClass,
    'Cost': CostClass,
    'CostCost': CostCostClass,
    'CostCostDiscriminator': CostCostDiscriminatorClass,
    'CostType': CostTypeClass,
    'Deprecation': DeprecationClass,
    'GlobalTags': GlobalTagsClass,
    'GlossaryTermAssociation': GlossaryTermAssociationClass,
    'GlossaryTerms': GlossaryTermsClass,
    'InstitutionalMemory': InstitutionalMemoryClass,
    'InstitutionalMemoryMetadata': InstitutionalMemoryMetadataClass,
    'MLFeatureDataType': MLFeatureDataTypeClass,
    'Owner': OwnerClass,
    'Ownership': OwnershipClass,
    'OwnershipSource': OwnershipSourceClass,
    'OwnershipSourceType': OwnershipSourceTypeClass,
    'OwnershipType': OwnershipTypeClass,
    'Status': StatusClass,
    'TagAssociation': TagAssociationClass,
    'VersionTag': VersionTagClass,
    'TransformationType': TransformationTypeClass,
    'UDFTransformer': UDFTransformerClass,
    'DashboardInfo': DashboardInfoClass,
    'DataFlowInfo': DataFlowInfoClass,
    'DataJobInfo': DataJobInfoClass,
    'DataJobInputOutput': DataJobInputOutputClass,
    'AzkabanJobType': AzkabanJobTypeClass,
    'DataProcessInfo': DataProcessInfoClass,
    'DatasetDeprecation': DatasetDeprecationClass,
    'DatasetFieldMapping': DatasetFieldMappingClass,
    'DatasetLineageType': DatasetLineageTypeClass,
    'DatasetProperties': DatasetPropertiesClass,
    'DatasetUpstreamLineage': DatasetUpstreamLineageClass,
    'Upstream': UpstreamClass,
    'UpstreamLineage': UpstreamLineageClass,
    'GlossaryNodeInfo': GlossaryNodeInfoClass,
    'GlossaryTermInfo': GlossaryTermInfoClass,
    'CorpGroupInfo': CorpGroupInfoClass,
    'CorpUserEditableInfo': CorpUserEditableInfoClass,
    'CorpUserInfo': CorpUserInfoClass,
    'ChartSnapshot': ChartSnapshotClass,
    'CorpGroupSnapshot': CorpGroupSnapshotClass,
    'CorpUserSnapshot': CorpUserSnapshotClass,
    'DashboardSnapshot': DashboardSnapshotClass,
    'DataFlowSnapshot': DataFlowSnapshotClass,
    'DataJobSnapshot': DataJobSnapshotClass,
    'DataProcessSnapshot': DataProcessSnapshotClass,
    'DatasetSnapshot': DatasetSnapshotClass,
    'GlossaryNodeSnapshot': GlossaryNodeSnapshotClass,
    'GlossaryTermSnapshot': GlossaryTermSnapshotClass,
    'MLFeatureSnapshot': MLFeatureSnapshotClass,
    'MLModelSnapshot': MLModelSnapshotClass,
    'TagSnapshot': TagSnapshotClass,
    'BaseData': BaseDataClass,
    'CaveatDetails': CaveatDetailsClass,
    'CaveatsAndRecommendations': CaveatsAndRecommendationsClass,
    'EthicalConsiderations': EthicalConsiderationsClass,
    'EvaluationData': EvaluationDataClass,
    'IntendedUse': IntendedUseClass,
    'IntendedUserType': IntendedUserTypeClass,
    'MLFeatureProperties': MLFeaturePropertiesClass,
    'MLModelFactorPrompts': MLModelFactorPromptsClass,
    'MLModelFactors': MLModelFactorsClass,
    'MLModelProperties': MLModelPropertiesClass,
    'Metrics': MetricsClass,
    'QuantitativeAnalyses': QuantitativeAnalysesClass,
    'SourceCode': SourceCodeClass,
    'SourceCodeUrl': SourceCodeUrlClass,
    'SourceCodeUrlType': SourceCodeUrlTypeClass,
    'TrainingData': TrainingDataClass,
    'MetadataChangeEvent': MetadataChangeEventClass,
    'ArrayType': ArrayTypeClass,
    'BinaryJsonSchema': BinaryJsonSchemaClass,
    'BooleanType': BooleanTypeClass,
    'BytesType': BytesTypeClass,
    'DatasetFieldForeignKey': DatasetFieldForeignKeyClass,
    'DateType': DateTypeClass,
    'EditableSchemaFieldInfo': EditableSchemaFieldInfoClass,
    'EditableSchemaMetadata': EditableSchemaMetadataClass,
    'EnumType': EnumTypeClass,
    'EspressoSchema': EspressoSchemaClass,
    'FixedType': FixedTypeClass,
    'ForeignKeySpec': ForeignKeySpecClass,
    'KafkaSchema': KafkaSchemaClass,
    'KeyValueSchema': KeyValueSchemaClass,
    'MapType': MapTypeClass,
    'MySqlDDL': MySqlDDLClass,
    'NullType': NullTypeClass,
    'NumberType': NumberTypeClass,
    'OracleDDL': OracleDDLClass,
    'OrcSchema': OrcSchemaClass,
    'OtherSchema': OtherSchemaClass,
    'PrestoDDL': PrestoDDLClass,
    'RecordType': RecordTypeClass,
    'SchemaField': SchemaFieldClass,
    'SchemaFieldDataType': SchemaFieldDataTypeClass,
    'SchemaMetadata': SchemaMetadataClass,
    'Schemaless': SchemalessClass,
    'StringType': StringTypeClass,
    'TimeType': TimeTypeClass,
    'UnionType': UnionTypeClass,
    'UrnForeignKey': UrnForeignKeyClass,
    'TagProperties': TagPropertiesClass,
}

_json_converter = avrojson.AvroJsonConverter(use_logical_types=False, schema_types=__SCHEMA_TYPES)

# fmt: on
