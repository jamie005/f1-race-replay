/// <reference types='vitest' />
import cesium from 'vite-plugin-cesium';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { nxViteTsPaths } from '@nx/vite/plugins/nx-tsconfig-paths.plugin';
import { nxCopyAssetsPlugin } from '@nx/vite/plugins/nx-copy-assets.plugin';
import { viteStaticCopy } from 'vite-plugin-static-copy'

export default defineConfig(() => ({
  root: __dirname,
  cacheDir: '../../node_modules/.vite/apps/f1-race-viewer',
  server: {
    port: 4200,
    host: '127.0.0.1',
  },
  preview: {
    port: 4300,
    host: '127.0.0.1',
  },
  plugins: [react(), nxViteTsPaths(), nxCopyAssetsPlugin(['*.md']),
    cesium({cesiumBuildPath: '../../node_modules/cesium/Build/Cesium'}),
    viteStaticCopy({
      targets: [
        {
          src: '../../node_modules/cesium/Build/Cesium/**',
          dest: 'cesium'
        }
      ]
    })
  ],
  // Uncomment this if you are using workers.
  // worker: {
  //  plugins: [ nxViteTsPaths() ],
  // },
  build: {
    outDir: '../../dist/apps/f1-race-viewer',
    emptyOutDir: true,
    reportCompressedSize: true,
    commonjsOptions: {
      transformMixedEsModules: true,
    },
  },
  test: {
    watch: false,
    globals: true,
    environment: 'jsdom',
    include: ['{src,tests}/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
    reporters: ['default'],
    coverage: {
      reportsDirectory: '../../coverage/apps/f1-race-viewer',
      provider: 'v8' as const,
    },
  },
}));
