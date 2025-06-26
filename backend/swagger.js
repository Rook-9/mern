// backend/swagger.js
import swaggerJSDoc from 'swagger-jsdoc';

const swaggerDefinition = {
  openapi: '3.0.0',
  info: {
    title: 'MERN Auth API',
    version: '1.0.0',
    description: 'API documentation for MERN Authentication app',
  },
  servers: [
    {
      url: 'http://localhost:5000',
    },
  ],
  components: {
    securitySchemes: {
      cookieAuth: {
        type: 'apiKey',
        in: 'cookie',
        name: 'jwt',
      },
    },
  },
  security: [
    {
      cookieAuth: [],
    },
  ],
};

const options = {
  swaggerDefinition,
  apis: ['./backend/routes/*.js'], // only parses JSDoc-style comments in this file
};

const swaggerSpec = swaggerJSDoc(options);

export default swaggerSpec;
