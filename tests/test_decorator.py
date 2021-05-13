"""
Test TLRUCache

:author: Angelo Cutaia
:copyright: Copyright 2021, Angelo Cutaia
:version: 1.0.0

..

    Copyright 2021 Angelo Cutaia

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

# Standard Library
import time

# Internal
from app.security.jwt_bearer import timed_lru_cache

# ------------------------------------------------------------------------------


@timed_lru_cache(1)
def fake_function(foo: str):
    """
    Fake function to test the decorator

    :param foo: value to use
    """
    time.sleep(0.5)
    return


def test_decorator():
    """
    Test if the decorator clean the cache after the expired time
    """
    # Call the first time
    now = time.time()
    fake_function("Foo")
    assert time.time() - now > 0.5

    # Call the second time
    now = time.time()
    fake_function("Foo")
    assert time.time() - now < 0.5

    # Call after the cache is expired
    time.sleep(0.5)
    now = time.time()
    fake_function("Foo")
    assert time.time() - now > 0.5
