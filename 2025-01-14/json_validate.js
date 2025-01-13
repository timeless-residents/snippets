const Ajv = require('ajv');
const addFormats = require('ajv-formats');

// AJVインスタンスを作成し、formatを追加
const ajv = new Ajv();
addFormats(ajv);

// JSONスキーマの定義
const schema = {
  type: 'object',
  properties: {
    name: { type: 'string', minLength: 1 },
    age: { type: 'number', minimum: 0 },
    email: { type: 'string', format: 'email' }
  },
  required: ['name', 'age']
};

// 検証用のデータ
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

// バリデーション実行
const validate = ajv.compile(schema);

// 有効なデータのテスト
const isValid1 = validate(validData);
console.log('Valid data:', isValid1);
console.log('Errors:', validate.errors);

// 無効なデータのテスト
const isValid2 = validate(invalidData);
console.log('Invalid data:', isValid2);
console.log('Errors:', validate.errors);