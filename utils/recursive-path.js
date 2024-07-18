const path = require("path");
const fs = require("fs");

function getPaths(filePath) {
  const entryPath = path.resolve(filePath);
  const entryPaths = [];

  // read the "entry file" content
  const fileContent = fs.readFileSync(entryPath, "utf8") + "";

  const paths = [];

  // get all include and extends paths
  // const pattern = /\{%\s*(include|extends)\s+["']?(.*?)["']?\s*%\}/g;
  const pattern = /\{%\s*(include|extends)\s+["']([^"']+?)["']\s*(?:\s+with\s+.+?)?\s*%\}/g;
  const matches = fileContent.matchAll(pattern);
  for (const match of matches) {
    const absolutePath = path.resolve(path.parse(entryPath).dir, match[2]);
    paths.push(absolutePath);
  }

  paths.forEach((item) => {
    entryPaths.push(...getPaths(item));
  });

  entryPaths.push(entryPath);

  return entryPaths;
}

module.exports = { getPaths };
