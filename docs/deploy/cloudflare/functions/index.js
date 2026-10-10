// Cloudflare Pages Function for the site root ("/").
// Sends visitors from Arabic-speaking countries to /ar/ and everyone else to /en/, using the
// country Cloudflare attaches to each request. A choice the visitor made earlier (cookie ag_lang,
// set by the language switch) always wins. If the country is unknown, the static gateway page
// (index.html) runs the same decision in the browser.
// Deploy: copy this "functions" folder next to index.html in the Cloudflare Pages project.
const ARABIC = new Set(["DZ", "BH", "KM", "DJ", "EG", "IQ", "JO", "KW", "LB", "LY", "MR", "MA", "OM", "PS", "QA", "SA", "SO", "SD", "SY", "TN", "AE", "YE", "EH", "TD"]);

export async function onRequest({ request, next }) {
  const cookie = request.headers.get("Cookie") || "";
  const saved = (cookie.match(/(?:^|;\s*)ag_lang=(ar|en)/) || [])[1];
  const cc = request.cf && request.cf.country;
  const lang = saved || (cc ? (ARABIC.has(cc) ? "ar" : "en") : null);
  if (!lang) return next();
  const target = new URL(`/${lang}/`, request.url).toString();
  return new Response(null, { status: 302, headers: { Location: target, "Vary": "Cookie", "Cache-Control": "private, no-store" } });
}
