install-npm:
	npm install

watch-tailwind:
	npm run watch-tailwind

run-flask:
	uv run der-duemmste

dev: install-npm
	make -j4 watch-tailwind run-flask

build-tailwind:
	npm run build-tailwind

prepare-deploy: install-npm build-tailwind

