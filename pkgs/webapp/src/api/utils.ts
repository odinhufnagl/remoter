import { toPairs } from "lodash";

export type ToQueryParams = Record<
  string,
  string | number | null | boolean | string[]
>;

export function objectToQueryParams(params?: ToQueryParams): string {
  const query = toPairs(params)
    .filter(([_, v]) => v !== null && v !== undefined)
    .map(([key, value]) => {
      if (Array.isArray(value)) {
        return `${key}=${encodeURIComponent(value.join(","))}`;
      }
      return `${key}=${encodeURIComponent(value as string)}`;
    })
    .filter((v) => v !== "")
    .join("&");
  return query ? `?${query}` : "";
}

export function queryParamsToObject(queryParams: string) {
  if (typeof queryParams !== "string") return {};

  const params = new URLSearchParams(queryParams);
  return (
    Array.from(params.keys()).reduce(
      (sum: Record<string, string | string[]>, key) => {
        if (!key || !params.get(key)) return sum;
        const value = sum[key] ? params.getAll(key) : params.get(key);
        return {
          ...sum,
          [key]: value !== null ? value : "",
        };
      },
      {}
    ) || {}
  );
}
