SOURCE_FILES := $(shell find . -name "*.py")

local: $(SOURCE_FILES)
	AWS_PROFILE=hackqc2019 pipenv run chalice local

deploy:
	AWS_PROFILE=hackqc2019 pipenv run chalice deploy

.PHONY: local deploy

