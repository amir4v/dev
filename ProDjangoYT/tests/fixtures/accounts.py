import pytest
from model_bakery import baker


@pytest.fixture
def key_pair():
	return dict(
		public='adfr34hf43dswer4',
		private='dk39fhg73hc83gvu',
	)


@pytest.fixture
def account_sender(key_pair):
	return baker.make(
		'accounts.Account',
		account='Amir',
		role='admin',
		key_pair=key_pair,
	)
