# Setup

1) Verificare la presenza di nvm sul sistema
```
nvm --version
```
Se non presente procedere all'installazione (si consiglia l'utilizzo di [brew](https://brew.sh/))

2) Abilitare la versione corretta di node
```
nvm use
```
Se ricevete un messaggio di errore riguardante la mancata presenza della versione corretta di node procedete all'installazione come suggerito dal messaggio

3) Installare a livello globale yarn, rimraf e vue cli
```
npm i -g yarn rimraf @vue/cli

yarn install
```

4) Procedere con il comando dedicato

### Frontend Development without django server
```
yarn v-serve
```

### Frontend Development with django server
```
yarn v-watch
```

### Deployment for development enviroment
```
yarn v-dev
```

### Deployment for stage enviroment
```
yarn v-stage
```

### Deployment for production enviroment
```
yarn v-prod
```

### Lint frontend project to use before any commit to solve issue
```
yarn v-lint
```

### Install storybook
```
npx sb init
```

This will update package json and and lockfile. Please install only if needed by the project


### Start storybook
```
yarn storybook
```


### Build storybook for production static website
```
yarn build-storybook
```
