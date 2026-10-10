// Netlify Edge Function for the site root ("/").
// Same rule as the gateway page: Arabic for Arabic-speaking countries, English elsewhere,
// and a saved choice (cookie ag_lang) always wins.
// Deploy: place this file in netlify/edge-functions/ at the root of the published site.
const ARABIC = new Set(["DZ", "BH", "KM", "DJ", "EG", "IQ", "JO", "KW", "LB", "LY", "MR", "MA", "OM", "PS", "QA", "SA", "SO", "SD", "SY", "TN", "AE", "YE", "EH", "TD"]);

export default async (request, context) => {
  const saved = context.cookies.get("ag_lang");
  const cc = context.geo && context.geo.country && context.geo.country.code;
  const lang = saved === "ar" || saved === "en" ? saved : (cc ? (ARABIC.has(cc) ? "ar" : "en") : null);
  if (!lang) return; // unknown: fall through to the gateway page
  return new Response(null, { status: 302, headers: { Location: `/${lang}/`, "Cache-Control": "private, no-store" } });
};

export const config = { path: "/" };
