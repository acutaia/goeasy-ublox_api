It is composed by U-Blox API, U-Blox Reader, and a dedicated PostgreSQL database deployed on
a Raspberry Pi 4 hardware, connected serially to a U-Blox receiver. The main purpose of this system is to
provide real-time and historical collections of trusted GALILEO navigation messages, to be used by the e-
Security Infrastructure components of the GOEASY Platform as reference values within the authentication
process of location-based data. The reference offered by the set of components quoted is verified through the
Position alteration detection library to guarantee that Galileo navigation messages received by the reference
system are not corrupted. The distributions of the reference systems among different country is necessary due
to the different visibility of the portion of sky, and consequently on the GALILEO satellites, at specific time and
location of the earth. The information provided by the reference systems are essential for the position
authentication algorithm executed on the GOEASY Platform. Through the mechanisms developed, the e-
Security Infrastructure can assure with a certain degree of confidence that third-party computed positions have
not been compromised without requiring additional computations on external applications that wants to exploit
such system. The overall technical documentation required by the developers is integrated in the source code
of each software component developed. In addition, it has been exploited automatic tools for grouping and
visualizing that information through static websites. To foster smooth integration and interoperability, each one
of the services built has been documented via open API specifications. Consequently, developers can exploit
these debugging features to test the REST-based API offered by the platform.