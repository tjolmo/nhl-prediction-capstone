import { useSearchParams } from "react-router-dom";

// NOT IMPLEMENTED YET
export default function SearchResultsPage() {
    const [searchParams] = useSearchParams();
    const query = searchParams.get("q") ?? "";

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100 font-sans p-4 sm:p-6 lg:p-10">
            <div className="max-w-5xl mx-auto">
                <h1 className="text-2xl font-black text-slate-800">
                    Search Results for{" "}
                    <span className="text-blue-600">"{query}"</span>
                </h1>
            </div>
        </div>
    );
}
