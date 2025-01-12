```jsx
// hello.ts
function greet(name: string): string {
    return `Hello, ${name}!`;
}

console.log(greet("World"));

// コンパイル後のJavaScript (hello.js)
// tsc hello.ts で生成される
function greet(name) {
    return "Hello, " + name + "!";
}
console.log(greet("World"));
```

TypeScriptでHello Worldプログラムを作成し、JavaScriptにコンパイルする例を示します。

上記のコードを実行するには:

1. TypeScriptをインストール:

```bash
npm install -g typescript

```

1. TypeScriptファイル（hello.ts）を作成し、上記のTypeScriptコードを保存
2. コンパイル実行:

```bash
tsc hello.ts

```

1. 生成されたJavaScriptを実行:

```bash
node hello.js

```

出力:

```
Hello, World!

```

このプログラムでは:

- TypeScriptで型付きの関数（greet）を定義しています（string型の引数を受け取り、string型を返す）
- コンパイルすると、型情報が削除されてピュアなJavaScriptになります
- テンプレートリテラル（`${}`）は通常の文字列連結に変換されます

なにか他に質問はありますか？