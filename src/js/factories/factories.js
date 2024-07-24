function addressFactory(obj) {
  const addr = {};

  if (obj?.cep) addr["cep"] = obj.cep;
  if (obj?.bairro) addr["district"] = obj.bairro;
  if (obj?.logradouro) addr["address"] = obj.logradouro;
  if (obj?.localidade) addr["locality"] = obj.localidade;
//   if (obj?.uf) addr["uf"] = obj.uf;
  if (obj?.numero) addr["number"] = obj.numero;
  if (obj?.complemento) addr["complement"] = obj.complemento;

  console.log(addr);
  return addr;
}

module.exports = {
  addressFactory,
};
