from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os


class BoostDiConan(ConanFile):
    name = "boost-di"
    license = "BSL-1.0"
    homepage = "https://github.com/boost-experimental/di"
    url = "https://github.com/conan-io/conan-center-index"
    description = "[Boost].DI: C++14 Dependency Injection Library."
    topics = ("dependency-injection", "metaprogramming", "design-patterns")
    exports_sources = ["patches/**"]
    settings = ("compiler",)
    options = {"with_extensions": [True, False], "diagnostics_level": [0, 1, 2]}
    default_options = {"with_extensions": False, "diagnostics_level": 1}
    no_copy_source = True

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def configure(self):
        minimal_cpp_standard = "14"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "5",
            "clang": "3.4",
            "apple-clang": "10",
            "Visual Studio": "15"
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                "%s recipe lacks information about the %s compiler standard version support" % (self.name, compiler))
            self.output.warn(
                "%s requires a compiler that supports at least C++%s" % (self.name, minimal_cpp_standard))
            return
        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s" % (self.name, minimal_cpp_standard))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "di-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

        if "patches" in self.conan_data and self.version in self.conan_data["patches"]:
            for patch in self.conan_data["patches"][self.version]:
                tools.patch(**patch)

    def package(self):
        self.copy("LICENSE_1_0.txt", src=self._source_subfolder, dst="licenses")
        if self.options.with_extensions:
            self.copy("*.hpp", src=os.path.join(self._source_subfolder, "extension", "include", "boost", "di", "extension"), dst=os.path.join("include", "boost", "di", "extension"), keep_path=True)
        self.copy("di.hpp", src=os.path.join(self._source_subfolder, "include", "boost"), dst=os.path.join("include", "boost"))

    def package_id(self):
        self.info.requires.clear()
        self.info.settings.clear()
        del self.info.options.diagnostics_level

    def package_info(self):
        self.cpp_info.defines.append("BOOST_DI_CFG_DIAGNOSTICS_LEVEL={}".format(self.options.diagnostics_level))
