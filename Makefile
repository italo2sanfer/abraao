
decrypt_password:
	@read -p "Enter password: " PASS; \
	python3 -c "from moises.utils import decrypt_password; print(decrypt_password('$(CODE)', '$$PASS'))"

set_passwd:
	@read -p "Enter password: " PASS; \
	python3 manage.py shell -c "from moises.utils import set_passwd; set_passwd('$(CODE)', '$$PASS')"
