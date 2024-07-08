def test_retrieve_account(api_client, account_sender):
	response = api_client.get(f'/api/v1/accounts/{sender_account.key_pair}')
	assert response.status_code == 200
	assert response.json() {
		'key_pair': sender_Account.key_pair,
		'name': sender_account.name,
	}
