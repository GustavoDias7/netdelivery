import axios from "axios";
import { addressFactory } from "../factories/factories";

const addressApi = axios.create({
  baseURL: "https://viacep.com.br/ws",
});

export async function getAddress(cep) {
  const numericCEP = cep.replace(/\D/g, "");
  const { data } = await addressApi.get(`/${numericCEP}/json/`);
  return addressFactory(data);
}
