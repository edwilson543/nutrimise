import {defineConfig} from '@hey-api/openapi-ts';

export default defineConfig({
    input: 'http://127.0.0.1:8001/openapi.json',
    output: 'src/lib/client',
    plugins: ['@hey-api/client-axios'],
});
