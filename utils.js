function extractExtendsPaths(htmlContent) {
    // Regular expression to match the path inside {% extends ... %}
    const pattern = /{%\s*extends\s*['"]([^'"]+)['"]\s*%}/g;
  
    // Array to store extracted paths
    const paths = [];
  
    // Using matchAll to find all matches
    const matches = htmlContent.matchAll(pattern);
  
    for (const match of matches) {
      paths.push(match[1]); // Push the first captured group (the path)
    }
  
    return paths;
  }
  function extractIncludePaths(htmlContent) {
    // Regular expression to match the path inside {% include ... %}
    const pattern = /{%\s*include\s*(['"])(.*?)\1\s*%}/g;
  
    // Array to store extracted paths
    const paths = [];
  
    // Using matchAll to find all matches
    const matches = htmlContent.matchAll(pattern);
  
    for (const match of matches) {
      paths.push(match[2]); // Push the second captured group (the path)
    }
  
    return paths;
  }
  module.exports = {extractExtendsPaths, extractIncludePaths}