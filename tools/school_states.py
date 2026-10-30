"""State school-staffing pages (CA, TX, MI, PA, IL, GA): page copy as data for build_pages.py."""

STATES = [
    # ── California ─────────────────────────────────────────────
    {
        "key": "ca",
        "name": "California",
        "file": "school-staffing-california.html",
        "title": "California School Staffing: SLP, OT, PT &amp; PPS | MedPoint Partners",
        "desc": "Contract SLPs, school psychologists, OTs, PTs and school nurses for California districts and SELPAs. CTC credentials checked first. Onsite or teletherapy.",
        "h1": "School Staffing in <em>California</em>",
        "hero": "Credentialed SLPs, PPS staff, OTs, PTs and school nurses for your district or SELPA, on contract for the school year or semester, onsite or by teletherapy.",
        "intro": [
            "The California Department of Education (CDE) oversees special education through its Special Education Division, under IDEA and the California Education Code. California calls related services <em>designated instruction and services</em>, or DIS. The DIS minutes in each IEP are what your district owes the student. They don’t stop when a position is open.",
            "These services are required by law and publicly funded. Credentials come from the Commission on Teacher Credentialing (CTC), and some roles also need a state board license. We staff on contract first, for the school year or the semester, and by teletherapy where it fits the student. Direct hire is available if you want to keep someone on.",
        ],
        "local": {
            "h": "SELPAs and county offices",
            "p": "Every California district takes part in a Special Education Local Plan Area (SELPA). A SELPA can be one large district, a group of districts, or districts joined with their county office of education, and each one works under a local plan approved by the CDE. Programs may sit with your district, another member district or the county office. Tell us who holds the caseload and where the students are, and we staff to that: one provider for one district, or one provider shared across sites.",
        },
        "creds": [
            ("slp", "School SLPs need the CTC’s Speech-Language Pathology Services Credential. The clear credential can be earned with a license from the Speech-Language Pathology &amp; Audiology &amp; Hearing Aid Dispensers Board, with the ASHA CCC, or with a passing Praxis score and a supervised fellowship."),
            ("psych", "School psychologists hold the CTC’s Pupil Personnel Services (PPS) credential with the school psychology specialization. School counselors and school social workers hold the same PPS credential in their own specializations."),
            ("ot", "School OTs and occupational therapy assistants are licensed by the California Board of Occupational Therapy."),
            ("pt", "School PTs and physical therapist assistants are licensed by the Physical Therapy Board of California."),
            ("nurse", "School nurses need a California RN license from the Board of Registered Nursing and the CTC’s School Nurse Services Credential. The preliminary credential requires a bachelor’s degree and the RN license; the clear credential adds a CTC-approved school nurse program and school nursing experience."),
            ("sped", "Special education teachers hold a CTC Education Specialist Instruction Credential in the area they teach, such as Mild to Moderate Support Needs or Extensive Support Needs."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can cover speech-language services, some counseling, and evaluation consults when the IEP team agrees it fits the student. The provider must hold the California credential or license the role requires for students located in California, wherever the provider lives. We confirm it before the candidate is sent.",
        "roles": ["slp", "psych", "ot", "pt", "nurse", "sped"],
        "faq": [
            ("Does a California school SLP need a CTC credential, a state license, or both?",
             "Districts look for the CTC’s Speech-Language Pathology Services Credential. A license from the Speech-Language Pathology &amp; Audiology &amp; Hearing Aid Dispensers Board is one route to the clear credential, and some SLPs hold both. We check the credential and the license before a candidate is sent."),
            ("What does DIS mean on a California IEP?",
             "Designated instruction and services is California’s term for related services, such as speech-language therapy, OT, PT and counseling. The DIS minutes written into the IEP are what your district owes, and what a MedPoint contract provider delivers while your position is open."),
            ("Can you staff for a SELPA or county office, not just one district?",
             "Yes. Tell us which agency holds the contract, the sites the role covers and how the caseload is split. MedPoint is employer of record for contract staff, so weekly payroll, taxes and workers’ comp are handled and you get one invoice."),
        ],
    },

    # ── Texas ──────────────────────────────────────────────────
    {
        "key": "tx",
        "name": "Texas",
        "file": "school-staffing-texas.html",
        "title": "Texas School Staffing: SLP, LSSP &amp; Diagnostician | MedPoint Partners",
        "desc": "Contract SLPs, diagnosticians, school psychologists (LSSPs), OTs and PTs for Texas districts and SSAs. Licenses checked first. Onsite or teletherapy.",
        "h1": "School Staffing in <em>Texas</em>",
        "hero": "SLPs, educational diagnosticians, school psychologists (LSSPs), OTs and PTs for your district or shared services arrangement, on contract first, onsite or by teletherapy.",
        "intro": [
            "The Texas Education Agency (TEA) oversees special education. In Texas the IEP team is the <em>ARD committee</em> (admission, review and dismissal), and only the ARD committee decides eligibility. That decision rests on the full and individual initial evaluation (FIIE), which often draws on an educational diagnostician, a school psychologist, an SLP, or all three.",
            "The services the ARD committee writes into the IEP are required under IDEA and Texas law, and they are publicly funded. When a seat is empty, the minutes and the evaluation timelines keep running. We staff those seats on contract for the school year or the semester, by teletherapy where it fits. Direct hire is there if you want to keep the person.",
        ],
        "local": {
            "h": "ESCs and shared services arrangements",
            "p": "Texas has 20 regional Education Service Centers (ESCs) that offer training, technical help and other services to the districts in their region. Districts can also join a special education shared services arrangement (SSA), where member districts pool staff and funds through one fiscal agent district. Contract staff fit either model. We can place a diagnostician with a single district, or an SLP who covers campuses across an SSA, with one invoice either way.",
        },
        "creds": [
            ("slp", "Texas SLPs are licensed by the Texas Department of Licensing and Regulation (TDLR). SLP assistants hold a TDLR assistant license and work under a licensed SLP’s supervision."),
            ("cfy", "Clinical fellows practice under a TDLR intern license, and the internship can’t start until the license is issued and the supervisor’s plan is approved. ASHA’s clinical fellowship can run at the same time, but only the Texas intern license allows practice in Texas."),
            ("diagnostician", "Educational diagnosticians hold a certificate from the State Board for Educator Certification (SBEC). It requires a master’s degree, a valid classroom teaching certificate, classroom teaching experience, an approved preparation program and a passing score on the TExES Educational Diagnostician exam."),
            ("psych", "School psychologists are licensed by the Texas State Board of Examiners of Psychologists, part of the Texas Behavioral Health Executive Council. The license was called Licensed Specialist in School Psychology (LSSP) until a 2025 law renamed it school psychologist without changing the requirements."),
            ("ot", "School OTs and OTAs are licensed by the Texas Board of Occupational Therapy Examiners, under the Executive Council of Physical Therapy &amp; Occupational Therapy Examiners."),
            ("pt", "School PTs and PTAs are licensed by the Texas Board of Physical Therapy Examiners, under the same executive council."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can deliver speech-language services and support evaluations and consults when the ARD committee agrees it fits the student. The provider must hold a Texas license for students located in Texas, wherever the provider lives: a TDLR license for an SLP, a Texas school psychologist license for psychological services. We confirm it before the candidate is sent.",
        "roles": ["slp", "diagnostician", "psych", "ot", "pt", "sped"],
        "faq": [
            ("Do you still staff LSSPs?",
             "Yes. In 2025 Texas renamed the Licensed Specialist in School Psychology license to school psychologist, but the requirements and the work stayed the same. Whatever your posting calls the role, we send candidates with an active license from the Texas State Board of Examiners of Psychologists."),
            ("Can a contract diagnostician help us catch up on FIIEs?",
             "Yes. A diagnostician on contract for the semester can take on initial evaluations and reevaluations to help keep your ARD meetings on schedule. Tell us the caseload and the deadlines, and we send a blinded shortlist in 48 to 72 hours."),
            ("Do you work with shared services arrangements?",
             "Yes. If your SSA’s fiscal agent holds the contract, we staff the role for the member districts on the caseload. MedPoint is employer of record, with weekly payroll, taxes and workers’ comp handled and one invoice."),
        ],
    },

    # ── Michigan ───────────────────────────────────────────────
    {
        "key": "mi",
        "name": "Michigan",
        "file": "school-staffing-michigan.html",
        "title": "Michigan School Staffing: SLP, OT &amp; Social Worker | MedPoint Partners",
        "desc": "Contract SLPs, school psychologists, school social workers, OTs and PTs for Michigan districts and ISDs. MDE and LARA credentials checked before we send anyone.",
        "h1": "School Staffing in <em>Michigan</em>",
        "hero": "SLPs, school psychologists, school social workers, OTs and PTs for your district or ISD, on contract for the school year or semester, onsite or by teletherapy.",
        "intro": [
            "The Michigan Department of Education (MDE) oversees special education through its Office of Special Education, under IDEA and the Michigan Administrative Rules for Special Education (MARSE). MARSE sets personnel requirements for school roles, so the right credential depends on the job, not just the degree.",
            "Eligibility starts with a multidisciplinary evaluation team (MET). The MET recommends, and the IEP team decides. The services in the IEP are required by law and publicly funded. We staff those roles on contract for the school year or the semester, by teletherapy where it fits, with direct hire available after.",
        ],
        "local": {
            "h": "Intermediate school districts",
            "p": "Michigan’s 56 intermediate school districts (some go by RESA, RESD or ESA) each file a plan with MDE for delivering special education in their area, and each levies a voter-approved special education millage. ISDs also run programs of their own, so related-service staff may work for the ISD or for a local district. Tell us who holds the caseload, and we contract with that agency.",
        },
        "creds": [
            ("slp", "Michigan school SLPs must meet MARSE’s personnel rule, starting with a master’s degree in speech-language pathology, and generally hold a license from the Michigan Board of Speech-Language Pathology through the Department of Licensing and Regulatory Affairs (LARA)."),
            ("psych", "School psychologists hold an MDE school psychologist certificate. The first step is the preliminary certificate; the full certificate requires a specialist-level program and internship."),
            ("socialworker", "School social workers need two credentials: an MDE school social worker credential, required for services under MARSE, and a master’s-level social work license from LARA."),
            ("ot", "School OTs are licensed through LARA’s Bureau of Professional Licensing."),
            ("pt", "School PTs are licensed through LARA’s Bureau of Professional Licensing."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can deliver speech-language services, some social work and counseling services, and evaluation consults when the IEP team agrees it fits. The provider must hold the Michigan license and any MDE credential the role requires for students located in Michigan, wherever the provider lives. We confirm both before the candidate is sent.",
        "roles": ["slp", "psych", "socialworker", "ot", "pt", "sped"],
        "faq": [
            ("Does a Michigan school social worker need an MDE credential and a LARA license?",
             "Yes. MDE requires a school social worker credential for services under MARSE, and that credential depends on a master’s-level social work license from LARA. We check both before a candidate is sent."),
            ("Do you work with ISDs as well as local districts?",
             "Yes. If the ISD runs the program or holds the caseload, we contract with the ISD. If a local district does, we contract with the district. Either way, MedPoint is employer of record: weekly payroll, taxes, workers’ comp and one invoice."),
            ("Can a contract school psychologist serve on our MET?",
             "Yes, if they hold the MDE school psychologist certificate. They can complete evaluations, write their part of the MET report and present it to the IEP team, onsite or, for the parts that suit it, by teletherapy."),
        ],
    },

    # ── Pennsylvania ───────────────────────────────────────────
    {
        "key": "pa",
        "name": "Pennsylvania",
        "file": "school-staffing-pennsylvania.html",
        "title": "Pennsylvania School Staffing: SLP, OT, PT &amp; Psych | MedPoint Partners",
        "desc": "Contract SLPs, school psychologists, social workers, nurses, OTs and PTs for Pennsylvania districts and IUs. PDE certificates and clearances checked first.",
        "h1": "School Staffing in <em>Pennsylvania</em>",
        "hero": "PDE-certified SLPs, school psychologists, school social workers and school nurses, plus licensed OTs and PTs, on contract for the school year or semester, onsite or by teletherapy.",
        "intro": [
            "The Pennsylvania Department of Education (PDE) oversees special education through its Bureau of Special Education, under IDEA and Chapter 14 of Title 22 of the Pennsylvania Code. Chapter 15 covers Section 504 service agreements. PaTTAN, the state’s training and technical assistance network, supports districts and intermediate units.",
            "In Pennsylvania the evaluation produces an Evaluation Report (ER), and the district proposes placement on a NOREP. The services in the IEP are required by law and publicly funded, and they continue when a position is open. We staff on contract for the school year or the semester first, by teletherapy where it fits, and offer direct hire after.",
        ],
        "local": {
            "h": "Intermediate units",
            "p": "Pennsylvania’s 29 intermediate units (IUs) are regional educational service agencies. Each IU files an annual special education plan with PDE, and IUs operate classes and related services for their member districts. Contract staff can be placed with an IU or directly with your district, depending on who runs the program.",
        },
        "creds": [
            ("slp", "School SLPs need PDE’s Educational Specialist certificate as a School Speech and Language Pathologist, PK-12. A license from the State Board of Examiners in Speech-Language Pathology and Audiology is a separate credential issued through the Department of State."),
            ("psych", "School psychologists hold PDE’s Educational Specialist certificate as a School Psychologist, PK-12."),
            ("socialworker", "Since August 1, 2026, a school social worker position must be filled by someone with PDE’s School Social Worker certificate, or by an LSW or LCSW on an emergency permit who is enrolled in an approved program. Home and School Visitor certificate holders can keep serving in that role but should not be titled school social workers."),
            ("nurse", "Certified school nurses hold PDE’s Educational Specialist certificate as a School Nurse, PK-12, along with a Pennsylvania RN license from the State Board of Nursing."),
            ("ot", "School OTs are licensed by the State Board of Occupational Therapy Education and Licensure."),
            ("pt", "School PTs are licensed by the State Board of Physical Therapy."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can deliver speech-language services and support evaluations and consults when the IEP team agrees it fits. The provider must hold the Pennsylvania certificate or license the role requires for students located in Pennsylvania, wherever the provider lives. We confirm it before the candidate is sent.",
        "roles": ["slp", "psych", "socialworker", "ot", "pt", "nurse"],
        "faq": [
            ("Do your contract staff get Pennsylvania clearances?",
             "Yes. Pennsylvania requires the State Police criminal history check (Act 34), the child abuse history clearance (Act 151) and the FBI fingerprint check (Act 114) for school contractors’ employees who have direct contact with students. We coordinate them before the start date, along with anything else your district requires."),
            ("We have a Home and School Visitor in a social work role. What changed?",
             "Since August 1, 2026, PDE requires a School Social Worker certificate for anyone in a school social worker position, with an emergency-permit route for licensed social workers enrolled in an approved program. If you need a certified school social worker for the rest of the year, we can staff the role on contract."),
            ("Can you staff an intermediate unit’s programs?",
             "Yes. We work with IUs and with districts directly. Tell us the classrooms, buildings and caseload the role covers, and we send a blinded shortlist in 48 to 72 hours, with PDE certificates and licenses checked first."),
        ],
    },

    # ── Illinois ───────────────────────────────────────────────
    {
        "key": "il",
        "name": "Illinois",
        "file": "school-staffing-illinois.html",
        "title": "Illinois School Staffing: SLP, OT &amp; Social Worker | MedPoint Partners",
        "desc": "Contract SLPs, school psychologists, school social workers, nurses, OTs and PTs for Illinois districts and co-ops. PEL endorsements and licenses checked first.",
        "h1": "School Staffing in <em>Illinois</em>",
        "hero": "SLPs, school psychologists, school social workers, school nurses, OTs and PTs for your district or cooperative, on contract for the school year or semester, onsite or by teletherapy.",
        "intro": [
            "The Illinois State Board of Education (ISBE) oversees special education under IDEA and the state’s special education rules, 23 Illinois Administrative Code Part 226. ISBE also issues the Professional Educator License (PEL). School support roles, including school psychologist, school social worker, school counselor, school nurse and speech-language pathologist, are added to the PEL as endorsements.",
            "Several related-service roles also need a license from the Illinois Department of Financial and Professional Regulation (IDFPR). The services in an IEP are required by law and publicly funded, whether your district delivers them or a cooperative does. We staff those roles on contract for the school year or the semester, by teletherapy where it fits, with direct hire available second.",
        ],
        "local": {
            "h": "Special education cooperatives",
            "p": "Illinois districts can pool special education through joint agreements, often called special education cooperatives. Each agreement is filed with ISBE and sets out the services, the governance and what each member district pays. Contract staff can be placed with the cooperative or with a member district, depending on who holds the caseload.",
        },
        "creds": [
            ("slp", "School SLPs need an SLP license from IDFPR and a PEL with ISBE’s speech-language pathologist school support personnel endorsement."),
            ("psych", "School psychologists hold a PEL with ISBE’s school psychologist endorsement, earned through a graduate program in school psychology and a school internship."),
            ("socialworker", "School social workers hold a PEL with the school social worker endorsement, which builds on a master’s in social work from a CSWE-accredited program and a school-based internship."),
            ("nurse", "School nurses with the PEL school nurse endorsement hold an Illinois RN license and a bachelor’s degree and have completed a supervised school nurse internship."),
            ("ot", "School OTs and occupational therapy assistants are licensed by IDFPR."),
            ("pt", "School PTs and physical therapist assistants are licensed by IDFPR."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can deliver speech-language services, some social work services, and evaluation consults when the IEP team agrees it fits. The provider must hold the Illinois license and PEL endorsement the role requires for students located in Illinois, wherever the provider lives. We confirm both before the candidate is sent.",
        "roles": ["slp", "psych", "socialworker", "nurse", "ot", "pt"],
        "faq": [
            ("Does an Illinois school SLP need both an IDFPR license and an ISBE endorsement?",
             "In practice, yes. The School Code builds the PEL speech-language pathologist endorsement on SLP licensure, so school SLPs carry an IDFPR license and the ISBE endorsement. We check both before a candidate is sent."),
            ("Can you staff a special education cooperative?",
             "Yes. We can contract with the cooperative or with a member district. Tell us the buildings and caseload the role covers. MedPoint is employer of record, with weekly payroll, taxes and workers’ comp handled and one invoice."),
            ("How fast can you send school social worker candidates?",
             "We send a blinded shortlist in 48 to 72 hours. Every candidate’s PEL school social worker endorsement is checked first, and every résumé arrives with answers to your screening questions."),
        ],
    },

    # ── Georgia ────────────────────────────────────────────────
    {
        "key": "ga",
        "name": "Georgia",
        "file": "school-staffing-georgia.html",
        "title": "Georgia School Staffing: SLP, OT &amp; School Psych | MedPoint Partners",
        "desc": "Atlanta-based school staffing for Georgia districts: contract SLPs, school psychologists, school social workers, OTs and PTs. GaPSC certificates checked first.",
        "h1": "School Staffing in <em>Georgia</em>",
        "hero": "SLPs, school psychologists, school social workers, OTs and PTs for Georgia districts from a team based in Atlanta, on contract first, onsite or by teletherapy.",
        "intro": [
            "The Georgia Department of Education (GaDOE) oversees special education through its Special Education Services and Supports division. Educator certification runs through the Georgia Professional Standards Commission (GaPSC), and clinical licenses through the state’s professional licensing boards.",
            "Every Georgia school has a Student Support Team (SST) that works on learning and behavior concerns, often before a special education referral. Once a student qualifies, the IEP services are required under IDEA and publicly funded. We staff them on contract for the school year or the semester first, by teletherapy where it fits, with direct hire available. MedPoint is based in Atlanta, so Georgia is home.",
        ],
        "local": {
            "h": "RESAs, GNETS and GLRS",
            "p": "Georgia’s 16 Regional Educational Service Agencies (RESAs) serve districts by region, and some act as fiscal agents for state special education programs. The Georgia Network for Educational and Therapeutic Support (GNETS) runs regional programs for students with severe emotional and behavioral disorders, and the Georgia Learning Resources System (GLRS) provides training and support. Contract staff can be placed with your district, or with the RESA or district that runs a regional program.",
        },
        "creds": [
            ("slp", "School SLPs hold a GaPSC service certificate in Speech and Language Pathology (P-12). Clinical licensure comes from the Secretary of State’s Speech-Language Pathology, Audiology, and Hearing Aid Dispensing Board, and a valid Georgia license or the ASHA CCC can count toward the certificate."),
            ("psych", "School psychologists hold a GaPSC School Psychology service certificate at the specialist (Level 6) level or higher, which requires a state-approved program and the GACE school psychology assessment."),
            ("socialworker", "School social workers hold a GaPSC School Social Work service certificate."),
            ("ot", "School OTs are licensed by the Georgia State Board of Occupational Therapy."),
            ("pt", "School PTs are licensed by the Georgia State Board of Physical Therapy."),
        ],
        "tele": "<a href=\"school-teletherapy-staffing.html\">Teletherapy</a> can deliver speech-language services and support evaluations and consults when the IEP team agrees it fits. The provider must hold the Georgia certificate or license the role requires for students located in Georgia, wherever the provider lives. We confirm it before the candidate is sent.",
        "roles": ["slp", "psych", "socialworker", "ot", "pt", "sped"],
        "faq": [
            ("Is MedPoint based in Georgia?",
             "Yes. MedPoint Partners, powered by NorthPoint, is based in Atlanta. We staff districts across Georgia, onsite or by teletherapy, and we check the GaPSC certificates and state licenses your roles call for before a candidate is sent."),
            ("Does a Georgia school SLP need a GaPSC certificate or a state license?",
             "Districts check for the GaPSC Speech and Language Pathology service certificate. The state license is a separate credential, and a valid Georgia license or the ASHA CCC is one route to the certificate. We check whichever your district requires."),
            ("Can you staff a GNETS program or a RESA?",
             "Yes. Tell us which agency holds the contract, the sites and the caseload. We place staff with the agency that runs the program, and MedPoint, as employer of record, sends one invoice."),
        ],
    },
]
