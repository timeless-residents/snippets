# JSON Schema Validation Example

Node.jsでAJV (Another JSON Validator) を使用したJSONスキーマバリデーションのサンプルコードです。

## 必要要件

- Node.js (v20.10.0以上推奨)
- npm

## セットアップ

1. 必要なパッケージをインストール:

```bash
npm install ajv ajv-formats
```

## 使用方法

1. `json_validate.js`を作成し、以下のコードを追加:

```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const ajv = new Ajv();
addFormats(ajv);

const schema = {
  type: 'object',
  properties: {
    name: { type: 'string', minLength: 1 },
    age: { type: 'number', minimum: 0 },
    email: { type: 'string', format: 'email' }
  },
  required: ['name', 'age']
};

const validData = {
  name: '山田太郎',
  age: 25,
  email: 'yamada@example.com'
};

const invalidData = {
  name: '',  // minLengthエラー
  age: -1,   // minimumエラー
  email: 'invalid-email'  // emailフォーマットエラー
};

const validate = ajv.compile(schema);

console.log('Valid data:', validate(validData));
console.log('Errors:', validate.errors);

console.log('Invalid data:', validate(invalidData));
console.log('Errors:', validate.errors);
```

2. スクリプトを実行:

```bash
node json_validate.js
```

## バリデーションルール

このサンプルでは以下のバリデーションを実装しています：

- `name`: 文字列、1文字以上必須
- `age`: 数値、0以上必須
- `email`: 文字列、メールアドレスフォーマット（オプション）

## エラー出力の例

バリデーションエラーが発生した場合、以下のような形式でエラー情報が出力されます：

```javascript
{
    instancePath: '/name',
    schemaPath: '#/properties/name/minLength',
    keyword: 'minLength',
    params: { limit: 1 },
    message: 'must NOT have fewer than 1 characters'
}
```

## エラーハンドリング

より実践的なエラーハンドリングの例：

```javascript
function validateUserData(data) {
    const valid = validate(data);
    if (!valid) {
        const errors = validate.errors.map(err => ({
            field: err.instancePath.substring(1),
            message: err.message,
            rule: err.keyword
        }));
        
        return {
            isValid: false,
            errors
        };
    }
    
    return {
        isValid: true,
        data
    };
}
```

## ライセンス

MIT

## 参考リンク

- [AJV Documentation](https://ajv.js.org/)
- [ajv-formats](https://github.com/ajv-validator/ajv-formats)