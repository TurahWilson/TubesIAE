# Patient Service

Microservice untuk mengelola data pasien menggunakan FastAPI + GraphQL.

## Endpoint
POST /graphql

## Contoh Query
```graphql
query {
  patients {
    id
    name
    phone
    address
  }
}
