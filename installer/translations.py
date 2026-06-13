"""
Multi-language translations for KernelMind GUI Installer.
Supported languages: English, Mandarin, Hindi, Spanish, French, Arabic, 
Bengali, Portuguese, Russian, German, Japanese, Indonesian.
"""

TRANSLATIONS = {
    "en": {
        "language": "English",
        "title": "KernelMind Installer",
        "license_label": "AGPL-3.0 License + PoE Ethics Clause",
        "accept_terms": "I accept AGPL-3.0 terms and commit to sharing modifications",
        "download_button": "Download from GitHub and Install",
        "modifications_label": "Describe your modifications (if this is a fork):",
        "modifications_placeholder": "Optional: describe changes you've made...",
        "status_downloading": "Downloading from GitHub...",
        "status_installing": "Installing dependencies...",
        "status_complete": "Ready to use! Run: km --help",
        "error_title": "Installation Error",
        "success_title": "Installation Successful",
        "success_message": "KernelMind installed successfully!\n\nNext steps:\n1. Run: km --help\n2. Try: km snapshot\n3. Start API: km-api\n4. View docs: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

Copyright (C) 2024-2026 Daniel Estefani / PoE Ecosystem

PREAMBLE

The GNU Affero General Public License is a free, copyleft license for
software and other kinds of works, specifically designed to ensure
cooperation with the community in the case of network server software.

The licenses for most software and other practical works are designed
to take away your freedom to share and change the works. By contrast,
our General Public Licenses are intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.

ADDITIONAL TERMS — PoE Ecosystem Ethical Clause
(permitted under AGPL-3.0 section 7)

Any derivative work of KernelMind must:

1. Preserve the EthicsLock module in its entirety and unmodified.
2. Not remove or weaken the human-confirmation requirement for
   TUNE, KILL, and DELETE action types.
3. Not enable NETWORK transmission of system data without explicit,
   per-session user consent.
4. Maintain the audit log (JSONL + SHA-256 fingerprint) for all
   non-READ actions.

These clauses reflect the foundational principles of the
Proof of Energy (PoE) ecosystem: transparency, reversibility,
and obligatory symbiosis between human and artificial intelligence.

For the complete license text, see:
https://www.gnu.org/licenses/agpl-3.0.en.html
""",
    },
    "zh": {
        "language": "中文 (Mandarin)",
        "title": "KernelMind 安装程序",
        "license_label": "AGPL-3.0 许可证 + PoE 伦理条款",
        "accept_terms": "我接受 AGPL-3.0 条款并承诺分享修改内容",
        "download_button": "从 GitHub 下载并安装",
        "modifications_label": "描述您的修改（如果这是一个分支）:",
        "modifications_placeholder": "可选：描述您所做的更改...",
        "status_downloading": "正在从 GitHub 下载...",
        "status_installing": "正在安装依赖项...",
        "status_complete": "准备就绪！运行：km --help",
        "error_title": "安装错误",
        "success_title": "安装成功",
        "success_message": "KernelMind 安装成功！\n\n后续步骤：\n1. 运行: km --help\n2. 尝试: km snapshot\n3. 启动 API: km-api\n4. 查看文档: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO 通用公共许可证
版本 3，2007 年 11 月 19 日

版权所有 © 2024-2026 Daniel Estefani / PoE 生态系统

前言

GNU AFFERO 通用公共许可证是一种自由的、左版的许可证，
专门为网络服务器软件而设计...

[Full Chinese translation of license]

PoE 生态系统伦理条款
（符合 AGPL-3.0 第 7 条）

KernelMind 的任何衍生作品必须：

1. 完整保留 EthicsLock 模块并保持不修改。
2. 不删除或削弱 TUNE、KILL 和 DELETE 操作类型的人类确认要求。
3. 未经显式的、按会话的用户同意，不启用网络传输系统数据。
4. 为所有非 READ 操作维护审计日志（JSONL + SHA-256 指纹）。

这些条款反映了 Proof of Energy (PoE) 生态系统的基本原则：
透明度、可逆性和人工智能与人类之间的强制共生。

完整许可证文本，请访问：
https://www.gnu.org/licenses/agpl-3.0.html
""",
    },
    "hi": {
        "language": "हिन्दी (Hindi)",
        "title": "KernelMind इंस्टॉलर",
        "license_label": "AGPL-3.0 लाइसेंस + PoE नैतिकता खंड",
        "accept_terms": "मैं AGPL-3.0 शर्तों को स्वीकार करता हूँ और संशोधन साझा करने के लिए प्रतिबद्ध हूँ",
        "download_button": "GitHub से डाउनलोड करें और इंस्टॉल करें",
        "modifications_label": "अपने संशोधनों का वर्णन करें (यदि यह एक कांटा है):",
        "modifications_placeholder": "वैकल्पिक: आपने जो परिवर्तन किए हैं उनका वर्णन करें...",
        "status_downloading": "GitHub से डाउनलोड किया जा रहा है...",
        "status_installing": "निर्भरताएं इंस्टॉल की जा रही हैं...",
        "status_complete": "उपयोग के लिए तैयार है! चलाएं: km --help",
        "error_title": "इंस्टॉलेशन त्रुटि",
        "success_title": "इंस्टॉलेशन सफल",
        "success_message": "KernelMind सफलतापूर्वक इंस्टॉल हो गया!\n\nअगले चरण:\n1. चलाएं: km --help\n2. आजमाएं: km snapshot\n3. API शुरू करें: km-api\n4. डॉक्स देखें: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO सामान्य सार्वजनिक लाइसेंस
संस्करण 3, 19 नवंबर 2007

कॉपीराइट © 2024-2026 Daniel Estefani / PoE पारिस्थितिकी तंत्र

[Hindi translation of full license text]
""",
    },
    "es": {
        "language": "Español (Spanish)",
        "title": "Instalador de KernelMind",
        "license_label": "Licencia AGPL-3.0 + Cláusula Ética PoE",
        "accept_terms": "Acepto los términos AGPL-3.0 y me comprometo a compartir modificaciones",
        "download_button": "Descargar de GitHub e Instalar",
        "modifications_label": "Describe tus modificaciones (si esta es una rama):",
        "modifications_placeholder": "Opcional: describe los cambios que has realizado...",
        "status_downloading": "Descargando desde GitHub...",
        "status_installing": "Instalando dependencias...",
        "status_complete": "¡Listo para usar! Ejecuta: km --help",
        "error_title": "Error de Instalación",
        "success_title": "Instalación Exitosa",
        "success_message": "¡KernelMind instalado exitosamente!\n\nPróximos pasos:\n1. Ejecuta: km --help\n2. Intenta: km snapshot\n3. Inicia API: km-api\n4. Ver documentación: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """LICENCIA PÚBLICA GENERAL AFFERO DE GNU
Versión 3, 19 de noviembre de 2007

Copyright © 2024-2026 Daniel Estefani / Ecosistema PoE

PREÁMBULO

La Licencia Pública General Affero de GNU es una licencia libre
y con copyleft, especialmente diseñada para asegurar la cooperación...

TÉRMINOS ADICIONALES - Cláusula Ética del Ecosistema PoE
(permitida bajo la sección 7 de AGPL-3.0)

Cualquier trabajo derivado de KernelMind debe:

1. Preservar el módulo EthicsLock en su totalidad y sin modificar.
2. No eliminar ni debilitar el requisito de confirmación humana
   para los tipos de acción TUNE, KILL y DELETE.
3. No permitir la transmisión de red de datos del sistema sin
   consentimiento explícito y por sesión del usuario.
4. Mantener el registro de auditoría (JSONL + huella SHA-256)
   para todas las acciones que no sean READ.

Para el texto completo de la licencia, visite:
https://www.gnu.org/licenses/agpl-3.0.es.html
""",
    },
    "fr": {
        "language": "Français (French)",
        "title": "Installateur KernelMind",
        "license_label": "Licence AGPL-3.0 + Clause Éthique PoE",
        "accept_terms": "J'accepte les termes AGPL-3.0 et m'engage à partager les modifications",
        "download_button": "Télécharger depuis GitHub et Installer",
        "modifications_label": "Décrivez vos modifications (si ceci est une fourche) :",
        "modifications_placeholder": "Optionnel: décrivez les changements que vous avez apportés...",
        "status_downloading": "Téléchargement depuis GitHub...",
        "status_installing": "Installation des dépendances...",
        "status_complete": "Prêt à l'emploi! Exécutez: km --help",
        "error_title": "Erreur d'Installation",
        "success_title": "Installation Réussie",
        "success_message": "KernelMind installé avec succès!\n\nÉtapes suivantes:\n1. Exécutez: km --help\n2. Essayez: km snapshot\n3. Démarrez API: km-api\n4. Voir docs: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """LICENCE PUBLIQUE GÉNÉRALE AFFERO GNU
Version 3, 19 novembre 2007

Droits d'auteur © 2024-2026 Daniel Estefani / Écosystème PoE

PRÉAMBULE

La Licence Publique Générale Affero GNU est une licence libre
et de gauche, spécialement conçue pour assurer la coopération...

TERMES SUPPLÉMENTAIRES - Clause Éthique de l'Écosystème PoE
(autorisée en vertu de la section 7 d'AGPL-3.0)

Toute œuvre dérivée de KernelMind doit:

1. Préserver le module EthicsLock dans son intégralité et sans modification.
2. Ne pas supprimer ni affaiblir l'exigence de confirmation humaine
   pour les types d'action TUNE, KILL et DELETE.
3. Ne pas permettre la transmission réseau de données système sans
   consentement explicite et par session de l'utilisateur.
4. Maintenir le journal d'audit (JSONL + empreinte SHA-256)
   pour toutes les actions autres que READ.

Pour le texte complet de la licence, visitez:
https://www.gnu.org/licenses/agpl-3.0.fr.html
""",
    },
    "ar": {
        "language": "العربية (Arabic)",
        "title": "مثبت KernelMind",
        "license_label": "ترخيص AGPL-3.0 + شرط أخلاقي PoE",
        "accept_terms": "أوافق على شروط AGPL-3.0 والتزم بمشاركة التعديلات",
        "download_button": "تحميل من GitHub وتثبيت",
        "modifications_label": "صف تعديلاتك (إذا كان هذا فرعاً):",
        "modifications_placeholder": "اختياري: صف التغييرات التي أجريتها...",
        "status_downloading": "جاري التحميل من GitHub...",
        "status_installing": "جاري تثبيت المتطلبات...",
        "status_complete": "جاهز للاستخدام! قم بتشغيل: km --help",
        "error_title": "خطأ في التثبيت",
        "success_title": "تم التثبيت بنجاح",
        "success_message": "تم تثبيت KernelMind بنجاح!\n\nالخطوات التالية:\n1. قم بتشغيل: km --help\n2. جرب: km snapshot\n3. ابدأ API: km-api\n4. عرض المستندات: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """ترخيص GNU AFFERO العام
الإصدار 3، 19 نوفمبر 2007

حقوق الطبع والنشر © 2024-2026 Daniel Estefani / نظام PoE البيئي

[Arabic translation of full license text]
""",
    },
    "bn": {
        "language": "বাংলা (Bengali)",
        "title": "KernelMind ইনস্টলার",
        "license_label": "AGPL-3.0 লাইসেন্স + PoE নৈতিকতা ধারা",
        "accept_terms": "আমি AGPL-3.0 শর্তাবলী গ্রহণ করি এবং সংশোধনগুলি শেয়ার করতে প্রতিশ্রুতিবদ্ধ",
        "download_button": "GitHub থেকে ডাউনলোড করুন এবং ইনস্টল করুন",
        "modifications_label": "আপনার সংশোধনগুলি বর্ণনা করুন (যদি এটি একটি ফর্ক হয়):",
        "modifications_placeholder": "ঐচ্ছিক: আপনি যে পরিবর্তনগুলি করেছেন তা বর্ণনা করুন...",
        "status_downloading": "GitHub থেকে ডাউনলোড করা হচ্ছে...",
        "status_installing": "নির্ভরতা ইনস্টল করা হচ্ছে...",
        "status_complete": "ব্যবহারের জন্য প্রস্তুত! চালান: km --help",
        "error_title": "ইনস্টলেশন ত্রুটি",
        "success_title": "ইনস্টলেশন সফল",
        "success_message": "KernelMind সফলভাবে ইনস্টল হয়েছে!\n\nপরবর্তী পদক্ষেপ:\n1. চালান: km --help\n2. চেষ্টা করুন: km snapshot\n3. API শুরু করুন: km-api\n4. ডক্স দেখুন: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO সাধারণ জনসাধারণ লাইসেন্স
সংস্করণ 3, 19 নভেম্বর 2007

কপিরাইট © 2024-2026 Daniel Estefani / PoE ইকোসিস্টেম

[Bengali translation of full license text]
""",
    },
    "pt": {
        "language": "Português (Portuguese)",
        "title": "Instalador KernelMind",
        "license_label": "Licença AGPL-3.0 + Cláusula Ética PoE",
        "accept_terms": "Aceito os termos da AGPL-3.0 e me comprometo a compartilhar modificações",
        "download_button": "Baixar do GitHub e Instalar",
        "modifications_label": "Descreva suas modificações (se for um fork):",
        "modifications_placeholder": "Opcional: descreva as alterações que você fez...",
        "status_downloading": "Baixando do GitHub...",
        "status_installing": "Instalando dependências...",
        "status_complete": "Pronto para usar! Execute: km --help",
        "error_title": "Erro na Instalação",
        "success_title": "Instalação Realizada com Sucesso",
        "success_message": "KernelMind instalado com sucesso!\n\nPróximos passos:\n1. Execute: km --help\n2. Teste: km snapshot\n3. Inicie API: km-api\n4. Veja a documentação: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """LICENÇA PÚBLICA GERAL AFFERO GNU
Versão 3, 19 de Novembro de 2007

Copyright © 2024-2026 Daniel Estefani / Ecossistema PoE

PREÂMBULO

A Licença Pública Geral Affero GNU é uma licença livre e com copyleft,
especialmente designada para garantir a cooperação...

TERMOS ADICIONAIS — Cláusula Ética do Ecossistema PoE
(permitida sob a seção 7 da AGPL-3.0)

Qualquer obra derivada do KernelMind deve:

1. Preservar o módulo EthicsLock em sua totalidade e sem modificações.
2. Não remover ou enfraquecer o requisito de confirmação humana
   para os tipos de ação TUNE, KILL e DELETE.
3. Não habilitar transmissão de rede de dados do sistema sem
   consentimento explícito e por sessão do usuário.
4. Manter o log de auditoria (JSONL + impressão digital SHA-256)
   para todas as ações que não sejam READ.

Para o texto completo da licença, visite:
https://www.gnu.org/licenses/agpl-3.0.pt-br.html
""",
    },
    "ru": {
        "language": "Русский (Russian)",
        "title": "Установщик KernelMind",
        "license_label": "Лицензия AGPL-3.0 + Этический пункт PoE",
        "accept_terms": "Я принимаю условия AGPL-3.0 и обязуюсь делиться модификациями",
        "download_button": "Загрузить с GitHub и установить",
        "modifications_label": "Опишите ваши модификации (если это форк):",
        "modifications_placeholder": "Дополнительно: опишите внесенные вами изменения...",
        "status_downloading": "Загрузка с GitHub...",
        "status_installing": "Установка зависимостей...",
        "status_complete": "Готово к использованию! Запустите: km --help",
        "error_title": "Ошибка установки",
        "success_title": "Установка успешна",
        "success_message": "KernelMind успешно установлен!\n\nСледующие шаги:\n1. Запустите: km --help\n2. Попробуйте: km snapshot\n3. Запустите API: km-api\n4. Смотрите документацию: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """УНИВЕРСАЛЬНАЯ ОБЩЕСТВЕННАЯ ЛИЦЕНЗИЯ GNU AFFERO
Версия 3, 19 ноября 2007 г.

Авторское право © 2024-2026 Daniel Estefani / Экосистема PoE

[Russian translation of full license text]
""",
    },
    "de": {
        "language": "Deutsch (German)",
        "title": "KernelMind-Installationsprogramm",
        "license_label": "AGPL-3.0-Lizenz + PoE-Ethikklausel",
        "accept_terms": "Ich akzeptiere die AGPL-3.0-Bedingungen und verpflichte mich, Änderungen zu teilen",
        "download_button": "Von GitHub herunterladen und installieren",
        "modifications_label": "Beschreiben Sie Ihre Änderungen (falls dies ein Fork ist):",
        "modifications_placeholder": "Optional: Beschreiben Sie die von Ihnen vorgenommenen Änderungen...",
        "status_downloading": "Wird von GitHub heruntergeladen...",
        "status_installing": "Abhängigkeiten werden installiert...",
        "status_complete": "Einsatzbereit! Führen Sie aus: km --help",
        "error_title": "Installationsfehler",
        "success_title": "Installation erfolgreich",
        "success_message": "KernelMind erfolgreich installiert!\n\nNächste Schritte:\n1. Führen Sie aus: km --help\n2. Versuchen Sie: km snapshot\n3. API starten: km-api\n4. Dokumentation anzeigen: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19. November 2007

Urheberrecht © 2024-2026 Daniel Estefani / PoE-Ökosystem

[German translation of full license text]
""",
    },
    "ja": {
        "language": "日本語 (Japanese)",
        "title": "KernelMind インストーラー",
        "license_label": "AGPL-3.0ライセンス + PoE倫理条項",
        "accept_terms": "AGPL-3.0の条件に同意し、修正内容の共有にコミットします",
        "download_button": "GitHubからダウンロードしてインストール",
        "modifications_label": "修正内容を説明してください（これがフォークの場合）:",
        "modifications_placeholder": "オプション：行った変更を説明してください...",
        "status_downloading": "GitHubからダウンロード中...",
        "status_installing": "依存関係をインストール中...",
        "status_complete": "使用可能です! 実行: km --help",
        "error_title": "インストールエラー",
        "success_title": "インストール成功",
        "success_message": "KernelMindがインストールされました！\n\n次のステップ:\n1. 実行: km --help\n2. 試す: km snapshot\n3. API開始: km-api\n4. ドキュメント表示: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """GNU AFFERO 一般公衆ライセンス
バージョン 3、2007年11月19日

著作権 © 2024-2026 Daniel Estefani / PoE エコシステム

[Japanese translation of full license text]
""",
    },
    "id": {
        "language": "Bahasa Indonesia (Indonesian)",
        "title": "Pemasang KernelMind",
        "license_label": "Lisensi AGPL-3.0 + Klausul Etika PoE",
        "accept_terms": "Saya menerima syarat AGPL-3.0 dan berkomitmen untuk berbagi modifikasi",
        "download_button": "Unduh dari GitHub dan Pasang",
        "modifications_label": "Jelaskan modifikasi Anda (jika ini adalah fork):",
        "modifications_placeholder": "Opsional: jelaskan perubahan yang Anda buat...",
        "status_downloading": "Mengunduh dari GitHub...",
        "status_installing": "Memasang dependensi...",
        "status_complete": "Siap digunakan! Jalankan: km --help",
        "error_title": "Kesalahan Instalasi",
        "success_title": "Instalasi Berhasil",
        "success_message": "KernelMind berhasil dipasang!\n\nLangkah berikutnya:\n1. Jalankan: km --help\n2. Coba: km snapshot\n3. Mulai API: km-api\n4. Lihat dokumentasi: https://github.com/armazen-nft/KERNEL-MIND",
        "license_text": """LISENSI PUBLIK UMUM AFFERO GNU
Versi 3, 19 November 2007

Hak Cipta © 2024-2026 Daniel Estefani / Ekosistem PoE

[Indonesian translation of full license text]
""",
    },
}

# Language code mapping
LANGUAGE_MAP = {
    "English": "en",
    "中文 (Mandarin)": "zh",
    "हिन्दी (Hindi)": "hi",
    "Español (Spanish)": "es",
    "Français (French)": "fr",
    "العربية (Arabic)": "ar",
    "বাংলা (Bengali)": "bn",
    "Português (Portuguese)": "pt",
    "Русский (Russian)": "ru",
    "Deutsch (German)": "de",
    "日本語 (Japanese)": "ja",
    "Bahasa Indonesia (Indonesian)": "id",
}

def get_language_code(display_name):
    """Get language code from display name."""
    return LANGUAGE_MAP.get(display_name, "en")

def get_translation(lang_code, key):
    """Get translated string for a key."""
    if lang_code not in TRANSLATIONS:
        lang_code = "en"
    return TRANSLATIONS[lang_code].get(key, TRANSLATIONS["en"].get(key, key))
