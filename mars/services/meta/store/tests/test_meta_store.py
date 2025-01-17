# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

import mars.tensor as mt
from mars.services.meta.store import get_meta_store


@pytest.mark.asyncio
async def test_mock_meta_store():
    meta_store = get_meta_store('mock')('mock_session_id')

    t = mt.random.rand(10, 10)
    t = t.tiles()

    await meta_store.set_tensor_meta(
        t.key, shape=t.shape, dtype=t.dtype,
        order=t.order, nsplits=t.nsplits)

    meta = await meta_store.get_tensor_meta(t.key, fields=['shape', 'order'])
    assert meta['shape'] == t.shape
    assert meta['order'] == t.order

    await meta_store.del_tensor_meta(t.key)

    with pytest.raises(KeyError):
        await meta_store.get_tensor_meta(t.key)
