export default function ProposalCard() {
    return (
        <div className="w-full rounded-2xl overflow-hidden bg-surface-light dark:bg-[#15261b] shadow-lg border border-gray-200 dark:border-primary/20">
            <div className="relative h-40 md:h-52 w-full overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent z-10" />
                <div
                    className="w-full h-full bg-cover bg-center"
                    style={{
                        backgroundImage:
                            "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBqC_uQaB_fCsD_B-BhOvy8WfnUufREXINi5-vsMZVx4xYpICl_DIRq61843DMZRXmux9ewS5ABOqCCmQkuHaWEl_JqndFWcrFv_YRlP_NBfTlpXjG5STtMS7sc-YIMcsk9X9M_DOUakZzbIBvHBzxxv3rG9NZjlq9KRryQrOQB1ssZNPlP_GFUZCy32l0P7fs40R2YIj6wLpJeP-AGlRH7txJGqWfZNV30MSqZodnTJIxR5d1KmwOuHE1q-BLTyRgHcCNFEK42EUAP')",
                    }}
                />
                <div className="absolute bottom-3 left-4 z-20">
                    <span className="px-2 py-1 rounded text-[10px] font-bold bg-primary text-[#102216] uppercase tracking-wider mb-1 inline-block">
                        Sugerencia
                    </span>
                    <h3 className="text-white text-lg font-bold">
                        Sustitución de Cena
                    </h3>
                </div>
            </div>

            <div className="p-5">
                <div className="flex flex-col md:flex-row gap-3 pt-2">
                    <button className="w-full md:flex-1 py-3 px-4 rounded-full bg-primary text-[#102216] text-sm font-bold">
                        Confirmar
                    </button>
                    <button className="w-full md:flex-1 py-3 px-4 rounded-full border text-sm font-bold">
                        Cancelar
                    </button>
                </div>
            </div>
        </div>
    );
}
