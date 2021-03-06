"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from json import dumps as json_to_str, loads as str_to_json
from cafe.engine.models.base import AutoMarshallingModel
from cloudcafe.meniscus.tenant_api.models.producer import Producer


class CreateTenant(AutoMarshallingModel):
    def __init__(self, tenant_id):
        super(CreateTenant, self).__init__()
        self.tenant_id = tenant_id

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {'tenant': {'tenant_id': self.tenant_id}}


class Tenant(AutoMarshallingModel):
    ROOT_TAG = 'tenant'

    def __init__(self, tenant_id=None, event_producers=None, token=None):
        """An object that represents an tenant's response object."""
        super(Tenant, self).__init__()
        self.tenant_id = tenant_id
        self.event_producers = event_producers
        self.token = token

    @classmethod
    def _json_to_obj(cls, serialized_str):
        """
        @param serialized_str:
        @return:
        """
        result = None
        json_dict = str_to_json(serialized_str)
        if json_dict is not None:
                result = [cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))]
        return result

    @classmethod
    def _dict_to_obj(cls, dic):
        event_producers = cls._convert_dict_of_types(
            Producer, dic.get('event_producers'))
        token = TenantToken._dict_to_obj(dic.get('token'))

        kwargs = {
            'tenant_id': str(dic.get('tenant_id')),
            'event_producers': event_producers,
            'token': token
        }
        return Tenant(**kwargs)

    @classmethod
    def _convert_dict_of_types(cls, c_type, dict):
        result = None
        if len(dict) > 0:
            result = []
            for item in dict:
                result.append(c_type._dict_to_obj(item))
        return result


class TenantToken(AutoMarshallingModel):

    def __init__(self, valid, previous, last_changed):
        super(TenantToken, self).__init__()
        self.valid = valid
        self.previous = previous
        self.last_changed = last_changed

    def _obj_to_json(self):
        return json_to_str(self._obj_to_dict())

    def _obj_to_dict(self):
        return {
            'valid': self.valid,
            'previous': self.previous,
            'last_changed': self.last_changed
        }

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = str_to_json(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return TenantToken(**json_dict)

    def __eq__(self, other):
        return self.valid != other.valid

    def __ne__(self, other):
        return not self == other


class ResetToken(AutoMarshallingModel):

    def __init__(self, invalidate_now=None):
        super(ResetToken, self).__init__()
        self.invalidate_now = invalidate_now

    def _obj_to_json(self):
        json_dict = {
            'token': {' invalidate_now': self.invalidate_now}
        }
        return json_to_str(json_dict)
